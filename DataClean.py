import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt




url = "C:\\Users\\rodri\\OneDrive - ISEG\\iseg 22092021\\Iseg\\Master\\2semester\\Big Data Tools and Analytics\\data\\city_temperature.csv"
temperature = pd.read_csv(url)




temperature= temperature.drop(columns=["State","Month", "Day"])




temperature




temperature = temperature[temperature["AvgTemperature"] != -99]
temperature = temperature[temperature["Year"] < 2020]




temperatureYear= temperature.groupby(['Year','Country'])




Temp=temperatureYear["AvgTemperature"].mean().reset_index()




Temp




#Temp["Year"] = pd.to_datetime(Temp["Year"])



plt.plot(Temp.Year, Temp.AvgTemperature)

plt.show()





url2="C:\\Users\\rodri\\OneDrive - ISEG\\iseg 22092021\\Iseg\\Master\\2semester\\Big Data Tools and Analytics\\data\\co2_data.csv"

co2 = pd.read_csv(url2)

co2



co2= co2.drop("consumption_co2","consumption_co2_per_capita","consumption_co2_per_gdp","","" )
list(co2.columns)

