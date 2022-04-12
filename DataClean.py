# Importing libraries -------------------------------------------------------------
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
# Importing Files ---------------------------------------------------------------

#rodrigo
#url = "C:\\Users\\rodri\\OneDrive - ISEG\\iseg 22092021\\Iseg\\Master\\2semester\\Big Data Tools and Analytics\\data\\city_temperature.csv"
#Joao
url = "C:\\Users\\joaod\\Desktop\\Big Data Tools\\Group Project\\city_temperature.csv"
#Rosanna
#url = "C:\\Users\\Rosan\\OneDrive - ISEG\\2 BDTA_Big Data Tools and Analytics\\Group Project\\Project Data\\city_temperature.csv"

temperature = pd.read_csv(url)

#Rodrigo
#url2="C:\\Users\\rodri\\OneDrive - ISEG\\iseg 22092021\\Iseg\\Master\\2semester\\Big Data Tools and Analytics\\data\\co2_data.csv"
#Joao
url2 = "C:\\Users\\joaod\\Desktop\\Big Data Tools\\Group Project\\co2_data.csv"
#Rosanna
#url2 = "C:\\Users\\Rosan\\OneDrive - ISEG\\2 BDTA_Big Data Tools and Analytics\\Group Project\\Project Data\\co2_data.csv"

co2 = pd.read_csv(url2)



# Cleaning Data ------------------------------------------------------------------

temperature= temperature.drop(columns=["State","Month", "Day"]) #dropping unnecessary columns
temperature = temperature[temperature["AvgTemperature"] != -99] #they put -99 for rows without info
temperature = temperature[temperature["Year"] < 2020] # there are very few rows available for 2020 onwards

temperatureYear= temperature.groupby(['Year']) #grouping temperature by year
Temp=temperatureYear["AvgTemperature"].mean().reset_index() #averging values for each year

co2_year = co2.groupby(["year"]) #grouping co2 by year
co2_overall = co2_year["co2"].mean().reset_index() #averaging values for each year

co2_95 = co2[co2["year"]>1994]
co2_95 = co2_95[co2_95["year"]<2020].groupby(["year"]) #matching co2 year range with the climate year range
co2_95_overall = co2_95["co2"].mean().reset_index() #averaging values for each year


# Question 1 -----------------------------------------------------------------
# How is the average temperature of the world changing over time and how steep is the temperature increase?
plt.plot(Temp.Year, Temp.AvgTemperature)
plt.xlabel('Year')
plt.ylabel('Average Temperature')
plt.title('Average Temperature plot over time')
plt.show()

# Question 2 ----------------------------------------------------------------
# How are the Co2 emissions of the world changing over time and how steep is the emission increase/decrease?
plt.plot(co2_95_overall.year, co2_95_overall.co2)
plt.xlabel('year')
plt.ylabel('Co2 Emissions')
plt.title('Co2 Emissions plot over time')
plt.show()


# Question 3 ----------------------------------------------------------------
# Which years had record temperatures? Are there also record Co2 emissions in those years?
temp_largest = Temp.nlargest(5, "AvgTemperature")
co2_largest = co2_95_overall.nlargest(5, "co2")

print(Temp.nlargest(5, "AvgTemperature"))
print(co2_95_overall.nlargest(5, "co2"))



































# Question 4 ----------------------------------------------------------------
#Which countries are making more effort to reduce Co2 emissions and which countries are making the least effort?

















































# Question 5 ----------------------------------------------------------------
# How does the Co2 emissions relate with the temperature changes? Is there a relation?
import statsmodels.api as sm














# Question 6 ----------------------------------------------------------------
# Question 7 ----------------------------------------------------------------
# Question 8 ----------------------------------------------------------------
# Question 9 ----------------------------------------------------------------
# Question 10 ----------------------------------------------------------------
# Question 11 ----------------------------------------------------------------
# Question 12 ----------------------------------------------------------------






















