![HDI Logo](thumb.jpg)
#Human Development Index Analysis Application
The aim of this project is to create an application which:
1. scrapes the most recent HDI score for each country from the Wikipedia HDI article;
2. gets the data for each country in the HDI list using restcountries API;
3. analyses the correlation between HDI score and countries’ characteristics;
4. saves the analysis result to [current_date].txt file.

## How To Use
To clone and install this application, you'll need Python and suitable IDE installed on your computer.
in addition to the following packages:
* From your command line:

* $ pip install requests
* $ pip install bs4
* $ pip install pandas
* $ pip install json

## Functionality

1. HDI data scrape from Wikipedia
Upon start the program:
* gets the contents of the List of countries by HDI webpage;
* parses the table with HDI and loads the data into the Pandas DataFrame 
  - columns: Country, HDI_score. using BeautifulSoup package with html.parser for that purpose.
    
2. Country Data via API
* After the web page is scraped the program gets the following data for each country in DataFrame.Country using the restcountries API:
- Population
- Area
- Gini
- Neighbours - number of neighbour countries.

3. Analysis \
The program utilizes the Pandas module and calculates the pairwise correlation between the DataFrame.HDI_score and each of the countries’ characteristics: Population, Area, Gini, Neighbours.
4. Reporting\
The program saves the results to [current_date].txt file and quits. The .txt report should look like this:\
   \
Correlation report:
   
|   | HDI score  |
|---|---|
|  Population |  0.435 |
| Area  |  0.125 |
|  Gini |  0.658 |
| Neighbours  | 0.125  |