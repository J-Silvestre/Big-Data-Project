import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt


# Importing Files ---------------------------------------------------------------
#rodrigo
url = "C:\\Users\\rodri\\OneDrive - ISEG\\iseg 22092021\\Iseg\\Master\\2semester\\Big Data Tools and Analytics\\data\\city_temperature.csv"
#Joao
#url = "C:\\Users\\joaod\\Desktop\\Big Data Tools\\Group Project\\city_temperature.csv"
#Rosanna

temperature = pd.read_csv(url)

#Rodrigo
url2="C:\\Users\\rodri\\OneDrive - ISEG\\iseg 22092021\\Iseg\\Master\\2semester\\Big Data Tools and Analytics\\data\\co2_data.csv"
#Joao
#url2 = "C:\\Users\\joaod\\Desktop\\Big Data Tools\\Group Project\\co2_data.csv"
#Rosanna

co2 = pd.read_csv(url2)



# Cleaning Data ------------------------------------------------------------------

temperature= temperature.drop(columns=["State","Month", "Day"]) #dropping unnecessary columns
temperature = temperature[temperature["AvgTemperature"] != -99] #they put -99 for rows without info
temperature = temperature[temperature["Year"] < 2020] # there are very few rows available for 2020 onwards
co2_95 = co2[co2["Year"]>1994] # matching co2 year range with the climate year range


# Question 1 -----------------------------------------------------------------

temperatureYear= temperature.groupby(['Year','Country'])

Temp=temperatureYear["AvgTemperature"].mean().reset_index()

Temp


plt.plot(Temp.Year, Temp.AvgTemperature)

plt.show()

#Temp["Year"] = pd.to_datetime(Temp["Year"])



# Question 2 ----------------------------------------------------------------
# Question 3 ----------------------------------------------------------------
# Question 4 ----------------------------------------------------------------
#Which countries are making more effort to reduce Co2 emissions and which countries are making the least effort?



# Question 5 ----------------------------------------------------------------
# Question 6 ----------------------------------------------------------------
# Question 7 ----------------------------------------------------------------
# Question 8 ----------------------------------------------------------------
# Question 9 ----------------------------------------------------------------
# Question 10 ----------------------------------------------------------------
# Question 11 ----------------------------------------------------------------
# Question 12 ----------------------------------------------------------------






















