# Loading the data

data_d1 <- scan('data_d1.csv')
data_d1

# converting it into time series
data_d1_timeseries <- ts(data_d1, frequency=12, start=c(2003,1))
data_d1_timeseries

# plotting the time series
plot.ts(data_d1_timeseries)

# taking log of time series
log_data_d1_timeseries <- log(data_d1_timeseries)
plot.ts(log_data_d1_timeseries)

library("TTR")
#install.packages('TTR')

# checking if our series has seasonal and trend component
data_d1_timeseries_components <- decompose(data_d1_timeseries)
data_d1_timeseries_components
data_d1_timeseries_components$seasonal
data_d1_timeseries_components$trend
data_d1_timeseries_components$random

# plot
plot(data_d1_timeseries_components)

# seasonal adjusting
data_d1_timeseries_seasonallyadjusted <- data_d1_timeseries - data_d1_timeseries_components$seasonal
plot(data_d1_timeseries_seasonallyadjusted)

# Holt-Winters Exponential Smoothing
ff = HoltWinters(data_d1_timeseries)
ff
ff$SSE
plot(ff)

library('forecast')
#install.packages('forecast')
future_forecast <- forecast.HoltWinters(ff, h=36)
future_forecast
plot.forecast(future_forecast)

future_forecast1 <- as.numeric(future_forecast$mean)
future_forecast1

data.set <- data.frame(future_forecast1)
data.set
future_forecast
plot.forecast(future_forecast)
future_forecast$residuals

############
acf(future_forecast$residuals, lag.max=20)
