import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd

# Pick the website to scrape
url = 'https://en.wikipedia.org/wiki/List_of_Game_of_Thrones_episodes'

# Get the response from the simple request
response = requests.get(url)

# Create a soup object
soup = bs4(response.text)

# Extract the last table with the viewing data

tables = soup.find_all('table', {'class': 'wikitable'})
table = tables[-1]

# get a list of the rows
rows_list = []

rows = table.find_all('tr')
for row in rows[2:]:
    rows_list.append(row)


final_lists=[]
row_values =[]
row_list =[]
for row in rows_list:
    row_list =[]
    
# Note that this takes the first cell in each row rather than reading across the row
    cells = row.find_all('td')
    for cell in cells: 
        value = cell.text
        if value != '–': # if the cell contains a '-' don't process it
            row_list.append(float(value)) # make the text a float number and add it to the list
    # Make sure there are 10 elements in the list to make the dataframe 10x8 elements      
    while len(row_list)<10:
        row_list.append(0.0)
    # only capture the data, not the average
    if len(row_list)>10:
        row_list = row_list[:10]
    final_lists.append(row_list) #add it to the final list of data 
    
    # create a DataFrame and save to CSV
    viewers = pd.DataFrame(final_lists)
    viewers.to_csv("viewer.csv", index = False)