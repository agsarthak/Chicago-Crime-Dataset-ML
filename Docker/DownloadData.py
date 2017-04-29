'''
Created on Apr 28, 2017

@author: Aashri
'''
import requests
import os
import shutil #to delete the directory contents
import pandas as pd
import boto.s3
import sys
from boto.s3.key import Key
import time
import datetime

argLen=len(sys.argv)
accessKey=''
secretAccessKey=''

for i in range(1,argLen):
    val=sys.argv[i]
    if val.startswith('accessKey='):
        pos=val.index("=")
        accessKey=val[pos+1:len(val)]
        continue
    elif val.startswith('secretKey='):
        pos=val.index("=")
        secretAccessKey=val[pos+1:len(val)]
        continue


print("Access Key=",accessKey)
print("Secret Access Key=",secretAccessKey)

############### Validate amazon keys ###############
if not accessKey or not secretAccessKey:
    print('Access Key and Secret Access Key not provided!!')
    exit()

AWS_ACCESS_KEY_ID = accessKey
AWS_SECRET_ACCESS_KEY = secretAccessKey

try:
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY)

    print("Connected to S3")

except:
    print("Amazon keys are invalid!!")
    exit()

if not os.path.exists('downloaded_csv'):
        os.makedirs('downloaded_csv', mode=0o777)
else:
    shutil.rmtree(os.path.join(os.path.dirname(__file__),'downloaded_csv'), ignore_errors=False)
    os.makedirs('downloaded_csv', mode=0o777)

url = 'https://data.cityofchicago.org/api/views/ijzp-q8t2/rows.csv?accessType=DOWNLOAD'

session_requests = requests.session()

r = session_requests.get(url,stream=True)
with open(os.path.join('downloaded_csv'), 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024):
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
            
####### Data preprocessing #######
data_crime = pd.read_csv('downloaded_csv/Crimes2001_to_present.csv')
data_crime.dropna(inplace=True)
data_crime.to_csv('')


#######Uploading to S3 ##########
try:   
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts)    
    bucket_name = AWS_ACCESS_KEY_ID.lower()+str(st).replace(" ", "").replace("-", "").replace(":","").replace(".","")
    bucket = conn.create_bucket(bucket_name)
    print("bucket created")
    zipfile = 'ChicagoCrimeData.zip'
    print ("Uploading %s to Amazon S3 bucket %s", zipfile, bucket_name)
    
    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()
    
    k = Key(bucket)
    k.key = 'ChicagoCrimeData'
    k.set_contents_from_filename(zipfile,
        cb=percent_cb, num_cb=10)
    print("Zip File successfully uploaded to S3")
except:
    print("Amazon keys are invalid!!")
    exit()


############ EOF ############