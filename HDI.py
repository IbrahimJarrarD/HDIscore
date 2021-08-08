import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

#HDI data scrape from Wikipedia
html = requests.get("https://en.wikipedia.org/wiki/List_of_countries_by_Human_Development_Index")
bsObj = BeautifulSoup(html.text, 'html.parser')

table_class = "wikitable sortable plainrowheaders"
big_table = bsObj.find('table', {'class': table_class})
df = pd.read_html(str(big_table), header=[0,1])
df = df[0]

#Cleaning the database
new_df = df.iloc[:, 2:4]f
new_df_columns = ["Country", "HDI_score"]
new_df.columns = new_df_columns
new_df.at[23, "Country"]= "Korea (Republic of)"
new_df.at[174, "Country"]= "Congo (Democratic Republic of the)"
new_df.at[148, "Country"]= "Congo-Brazzaville"
new_df.at[125, "Country"]= 'Cabo Verde'
new_df.at[81, "Country"]="Macedonia (the former Yugoslav Republic of)"
new_df.at[12, "Country"]= "United Kingdom of Great Britain and Northern Ireland"
new_df.at[16, "Country"]="United States of America"
new_df.at[46, "Country"]="Brunei Darussalam"
new_df.at[51, "Country"]="Russian Federation"
new_df.at[70, "Country"]="Iran (Islamic Republic of)"
new_df.at[89, "Country"]="Moldova (Republic of)"
new_df.at[106, "Country"]="Bolivia (Plurinational State of)"
new_df.at[112, "Country"]="Venezuela (Bolivarian Republic of)"
new_df.at[114, "Country"]="Palestine, State of"
new_df.at[117, "Country"]="Viet Nam"
new_df.at[135, "Country"]="Micronesia (Federated States of)"
new_df.at[137, "Country"]="Swaziland"
new_df.at[151, "Country"]="Syrian Arab Republic"
new_df.at[162, "Country"]="Tanzania, United Republic of"


#Getting the API data
import json
response = requests.get("https://restcountries.eu/rest/v2/all")
responseJson = json.loads(response.text)
#Our lists to save values
list_population = []
list_names = []
list_gini = []
#Will not be using this as it still needs to be calculated
list_neighbours = []
list_area = []

#nested loops to compare our country data
for country in new_df["Country"]:
    reason = requests.get("https://restcountries.eu/rest/v2/name/{}".format(country))
    reasonJson = json.loads(reason.text)
    for country1 in reasonJson:
        if (country == country1['name']) or (country == country1['topLevelDomain']) or (country in country1['altSpellings']) or (country in country1['alpha2Code']):
            list_population.append(country1['population'])
            list_names.append(country1['name'])
            list_gini.append(country1["gini"])
            list_neighbours.append(country1["borders"])
            list_area.append(country1["area"])


#Calulating the number of neighbours
neighbours_number = []
for list in list_neighbours:
    neighbours_number.append(len(list))


#Creating the DataFrame from the RestAPI
df = pd.DataFrame({"Population": list_population,
                   "Gini" : list_gini,
                   "Number_of_Neighbours": neighbours_number,
                   "Area": list_area
                   })

#Merging the 2 Dataframes

df_complete = pd.concat([new_df, df], axis=1)
df_complete.dropna(axis=0)

# Seperating the columns to prepare for the correlations
column_population = df_complete["Population"]
column_gini = df_complete["Gini"]
column_area = df_complete["Area"]
column_neighbours = df_complete["Number_of_Neighbours"]
# Calculating the correlations
hdi_on_population = df_complete["HDI_score"].corr(column_population)
hdi_on_gini = df_complete["HDI_score"].corr(column_gini)
hdi_on_area = df_complete["HDI_score"].corr(column_area)
hdi_on_neighbours =  df_complete["HDI_score"].corr(column_neighbours)




#file with date of today
exportFilename = str(datetime.date.today())
with open(str(exportFilename)+'.txt', 'w') as file:
    file.write("""Correlation report\n 
                                   HDI score\n
                population        {}
                Area              {}
                Gini              {}
                Neighbours        {}""".format(hdi_on_population, hdi_on_area, hdi_on_gini, hdi_on_neighbours))

file.close()
