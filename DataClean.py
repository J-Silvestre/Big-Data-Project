# Importing libraries -------------------------------------------------------------
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import statsmodels.api as sm







# Importing Files ---------------------------------------------------------------

#rodrigo
url = "C:\\Users\\rodri\\OneDrive - ISEG\\iseg 22092021\\Iseg\\Master\\2semester\\Big Data Tools and Analytics\\data\\city_temperature.csv"
#Joao
#url = "C:\\Users\\joaod\\Desktop\\Big Data Tools\\Group Project\\city_temperature.csv"
#Rosanna
#url = "C:\\Users\\Rosan\\OneDrive - ISEG\\2 BDTA_Big Data Tools and Analytics\\Group Project\\Project Data\\city_temperature.csv"

temperature = pd.read_csv(url)

#Rodrigo
url2="C:\\Users\\rodri\\OneDrive - ISEG\\iseg 22092021\\Iseg\\Master\\2semester\\Big Data Tools and Analytics\\data\\co2_data.csv"
#Joao
#url2 = "C:\\Users\\joaod\\Desktop\\Big Data Tools\\Group Project\\co2_data.csv"
#Rosanna
#url2 = "C:\\Users\\Rosan\\OneDrive - ISEG\\2 BDTA_Big Data Tools and Analytics\\Group Project\\Project Data\\co2_data.csv"

co2 = pd.read_csv(url2)



# Cleaning Data ------------------------------------------------------------------
temperature= temperature.drop(columns=["State","Month", "Day"]) #dropping unnecessary columns
temperature = temperature[temperature["AvgTemperature"] != -99] #they put -99 for rows without info
temperature = temperature[temperature["Year"] < 2020] # there are very few rows available for 2020 onwards

temperatureYear= temperature.groupby(['Year']) #grouping temperature by year
Temp=temperatureYear["AvgTemperature"].mean().reset_index() #averging values for each year

co2= co2[["iso_code","country","year","co2","consumption_co2","co2_growth_prct","co2_growth_abs","co2_per_capita","gdp", "population"]]
co2["id"] = co2.index
co2=co2.set_index("id")
co2_country= co2.groupby("country")
co2_year = co2.groupby(["year"]) #grouping co2 by year
co2_overall = co2_year["co2"].mean().reset_index() #averaging values for each year

co2_95 = co2[co2["year"]>1994]
co2_95 = co2_95[co2_95["year"]<2020].groupby(["year"]) #matching co2 year range with the climate year range
co2_95_overall = co2_95["co2"].mean().reset_index() #averaging values for each year
co2Abs= co2_country.mean().reset_index()

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
plt.xlabel('Year')
plt.ylabel('Co2 Emissions')
plt.title('Co2 Emissions plot over time')
plt.show()


# Question 3 ----------------------------------------------------------------
# Which years had record temperatures? Are there also record Co2 emissions in those years?
co2_largest = co2_95_overall[co2_95_overall["year"]>2011]
temp_largest = Temp[Temp["Year"]>2011]

ax1 = co2_largest.co2.plot(color='blue', grid=True, label='Co2 Emissions')
ax2 = temp_largest.AvgTemperature.plot(color='red', grid=True, secondary_y=True, label='Average Temperature')
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
plt.legend(h1+h2, l1+l2, loc=2)
plt.xlabel('Year')
plt.show()


# Question 4 ----------------------------------------------------------------
#Which countries are making more effort to reduce Co2 emissions and which countries are making the least effort?

#Find the countries with the highest values for co2

co2Abs.sort_values(by = "co2", ascending = False).head(20)

#Create a data frame for the top 5 countries
co2AbsChina= co2[co2["country"]== "China"]
co2AbsUsa= co2[co2["country"]== "United States"]
co2AbsGermany= co2[co2["country"]== "Germany"]
co2AbsRussia= co2[co2["country"]== "Russia"]
co2AbsJapan= co2[co2["country"]== "Japan"]

#Creating a plot for top 5 country
plt.plot(co2AbsChina.year, co2AbsChina.co2, label = "China")
plt.plot(co2AbsUsa.year, co2AbsUsa.co2, label = "USA")
plt.plot(co2AbsGermany.year, co2AbsGermany.co2, label = "Germany")
plt.plot(co2AbsRussia.year, co2AbsRussia.co2, label = "Russia")
plt.plot(co2AbsJapan.year, co2AbsJapan.co2, label = "Japan")
plt.xlabel('Year')
plt.ylabel('Co2')
plt.title("Co2 production in top 5 countries")
plt.legend()
plt.show()


# Question 5 ----------------------------------------------------------------
# How does the Co2 emissions relate with the temperature changes? Is there a relation?

# Fit a linear regression model and calculate the R-square
x = co2_95_overall["co2"] #co2 as independent variable
y = Temp["AvgTemperature"] #temperature as dependent variable

x1 = sm.add_constant(x)
model = sm.OLS(y, x1)
result = model.fit()
z = result.predict(x1)
result.summary()

# Plot linear regression model and effective data
fig, ax = plt.subplots(figsize=(8,6))
plt.xlabel('co2 (in million tonnes)')
plt.ylabel('Average Temperature (in Fahrenheit)')
plt.title('Linear Regression Model')
ax.plot(x, y, "o")
ax.plot(x, z, "-")
plt.xlabel('Year')
plt.ylabel('Co2')
plt.title("Co2 production in top 5 countries")
plt.legend()
plt.show()

# Question 6 ----------------------------------------------------------------
#Are the countries with the highest temperature increase, the countries which pollute most?


#group the temperature by country and year
temperature_year_country=temperature.groupby(['Year','Country'])

#getting the average temperature for each key
Temp_country=temperature_year_country["AvgTemperature"].mean().reset_index()

#sort the values 
Temp_country= Temp_country.sort_values(by=["Country","Year"])

#Create a new index to replace
Index=[]
for i in range(len(Temp_country["Year"])):
    Index.append(i)
#Adding the index to new data frame   
Temp_country["Index"]= Index
Temp_country=Temp_country.set_index("Index")

#create a new column with empty values
Temp_growth=[]
for i in range(len(Temp_country["Year"])):
    Temp_growth.append(0)
Temp_country["Temp_growth"]= Temp_growth    
    
    

#Create loop to add temperature growth column
for i in range(1, len(Temp_country)):
    if i == 0:
        Temp_country["Temp_growth"][i]= np.nan
        continue
    if Temp_country["Country"][i] == Temp_country["Country"][i-1]:
        Temp_country["Temp_growth"][i] = (Temp_country["AvgTemperature"][i] - Temp_country["AvgTemperature"][i-1])/100
    else:
        Temp_country["Temp_growth"][i]= np.nan


#Gets rid of the nan created purposely
Temp_country= Temp_country.dropna()
Temp_country= Temp_country.drop(0, axis = 0)

#Gives the biggest temperature growth changes that happened.
Temp_country.sort_values(by= "Temp_growth", ascending= False).head(30)

#Creating objects for the countries with the biggest changes in last years


AvgBelgium=Temp_country[Temp_country["Country"]== "Belgium"]
AvgCyprus= Temp_country[Temp_country["Country"]== "Cyprus"]
AvgKyrgyzstan= Temp_country[Temp_country["Country"]== "Kyrgyzstan"]
AvgUnited_States= Temp_country[Temp_country["Country"]== "US"]
AvgEquador= Temp_country[Temp_country["Country"]== "Equador"]
AvgNorway= Temp_country[Temp_country["Country"]== "Norway"]
AvgUK= Temp_country[Temp_country["Country"]== "United Kingdom"]
AvgChina = Temp_country[Temp_country["Country"]== "China"]

plt.plot(AvgBelgium.Year, AvgBelgium.AvgTemperature, label = "Belgium")
plt.plot(AvgKyrgyzstan.Year, AvgKyrgyzstan.AvgTemperature, label ="Kyrgyzstan")
plt.plot(AvgUnited_States.Year, AvgUnited_States.AvgTemperature, label= "USA")
plt.plot(AvgEquador.Year, AvgEquador.AvgTemperature, label ="Equador")
plt.plot(AvgNorway.Year, AvgNorway.AvgTemperature, label = "Norway")
plt.plot(AvgUK.Year, AvgUK.AvgTemperature, label = "Uk")
plt.plot(AvgChina.Year, AvgChina.AvgTemperature, label= "China")
plt.xlabel('Year')
plt.ylabel('Average temperature')
plt.title("Temperature changes in some countries")
plt.legend(loc=2)
plt.show()






























# Question 7 ----------------------------------------------------------------
# Do the countries that emit the most Co2 overall, coincide with the countries that emit the most Co2 per capita?

# Create a dataframe with top 5 countries for average co2 production over all years
co2_top20 = co2Abs.sort_values(by = "co2", ascending = False).head(20)
co2_top5Countries = ["China", "United States", "Germany", "Russia", "Japan"]

df_co2_top5Countries = co2_top20[co2_top20.country.isin(co2_top5Countries)]

# Create a dataframe with top 5 countries for average co2/capita over all years
co2pCapita_top20 = co2Abs.sort_values(by = "co2_per_capita", ascending = False).head(20)
co2pCapita_top5Countries = ["Sint Maarten (Dutch part)", "Curacao", "Qatar", "Bonaire Sint Eustatius and Saba", "United Arab Emirates"]

df_co2pCapita_top5Countries = co2pCapita_top20[co2pCapita_top20.country.isin(co2pCapita_top5Countries)]

# Plot bar chart for top 5 Countries of co2
plt.bar(df_co2_top5Countries.country, df_co2_top5Countries.co2)

# Plot bar chart for top 5 Countries of co2 per Capita
plt.bar(df_co2pCapita_top5Countries.country, df_co2pCapita_top5Countries.co2_per_capita)














# Question 8 ----------------------------------------------------------------
# Do countries with higher GDP pollute more?
co2GDPChina= co2[co2["country"]== "China"]
co2GDPChina = co2GDPChina[co2GDPChina["year"]>1994].dropna()

co2GDPUsa= co2[co2["country"]== "United States"]
co2GDPUsa = co2GDPUsa[co2GDPUsa["year"]>1994].dropna()

co2GDPIndia= co2[co2["country"]== "India"]
co2GDPIndia = co2GDPIndia[co2GDPIndia["year"]>1994].dropna()

co2GDPRussia= co2[co2["country"]== "Russia"]
co2GDPRussia = co2GDPRussia[co2GDPRussia["year"]>1994].dropna()

co2GDPJapan= co2[co2["country"]== "Japan"]
co2GDPJapan = co2GDPJapan[co2GDPJapan["year"]>1994].dropna()

plt.plot(co2GDPJapan.year, co2GDPChina.gdp, label = "China")
plt.plot(co2GDPJapan.year, co2GDPUsa.gdp, label = "USA")
plt.plot(co2GDPJapan.year, co2GDPIndia.gdp, label = "India")
plt.plot(co2GDPJapan.year, co2GDPRussia.gdp, label = "Russia")
plt.plot(co2GDPJapan.year, co2GDPJapan.gdp, label = "Japan")
plt.xlabel('Year')
plt.ylabel('gdp')
plt.title("gdp production in top 5 countries")
plt.legend()
plt.xlim([1995, 2018])
plt.show()



# Question 9 -----------------------------------------------------------------
# Which countries pollute the most and which countries pollute the least? 
# How is this changing over time?

#5largest: Qatar, United Arab Emirates, Saudi Arabia, Australia, United States
#Create a data frame for the upper 5 countries
co2_Q= co2[co2["country"]== "Qatar"]
co2_UAE= co2[co2["country"]== "United Arab Emirates"]
co2_SA= co2[co2["country"]== "Saudi Arabia"]
co2_AUS= co2[co2["country"]== "Australia"]
co2_USA= co2[co2["country"]== "United States"]
#Creating a plot for top 5 country
plt.plot(co2_Q.year, co2_Q.co2_per_capita, label = "Qatar")
plt.plot(co2_UAE.year, co2_UAE.co2_per_capita, label = "UAE")
plt.plot(co2_SA.year, co2_SA.co2_per_capita, label = "Saudi Arabia")
plt.plot(co2_AUS.year, co2_AUS.co2_per_capita, label = "Australia")
plt.plot(co2_USA.year, co2_USA.co2_per_capita, label = "USA")
plt.xlabel('Year')
plt.ylabel('Co2 per capita')
plt.title("Co2 per capita production in top 5 countries")
plt.legend()
plt.xlim([1980, 2018])
plt.show()


#5smallest: Democratic Republic of Congo, Burundi, Central African Republic, Somalia, Chad
#Create a data frame for the lower 5 countries
co2_DRC= co2[co2["country"]== "Democratic Republic of Congo"]
co2_B= co2[co2["country"]== "Burundi"]
co2_CAR= co2[co2["country"]== "Central African Republic"]
co2_S= co2[co2["country"]== "Somalia"]
co2_C= co2[co2["country"]== "Chad"]
#Creating a plot for lowest 5 country
plt.plot(co2_DRC.year, co2_DRC.co2_per_capita, label = "Congo")
plt.plot(co2_B.year, co2_B.co2_per_capita, label = "Burundi")
plt.plot(co2_CAR.year, co2_CAR.co2_per_capita, label = "Central Africa")
plt.plot(co2_S.year, co2_S.co2_per_capita, label = "Somalia")
plt.plot(co2_C.year, co2_C.co2_per_capita, label = "Chad")
plt.xlabel('Year')
plt.ylabel('Co2 per capita')
plt.title("Co2 per capita production in top 5 countries")
plt.legend()
plt.xlim([1980, 2018])
plt.show()



# Question 10 ----------------------------------------------------------------
# Question 11 ----------------------------------------------------------------
# Question 12 ----------------------------------------------------------------


















