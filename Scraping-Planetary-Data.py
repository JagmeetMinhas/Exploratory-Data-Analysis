import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = "https://nssdc.gsfc.nasa.gov/planetary/factsheet/"
getReq = requests.get(url)

attributeList = []
planetList = []
rowList = []
tableList = []

d = {}

sourceCode = BeautifulSoup(getReq.content, 'html.parser')

for tag in sourceCode.find_all("tr"):
    headers = tag.find("td", attrs = {"align": "left"})
    attribute = headers.find("a")
    if attribute is not None:
        attributeList.append(attribute.get_text())
        d[attribute.get_text()] = None
    
    data = tag.find_all("td", attrs = {"align": "center"})
    for tag in data:
        planetTag = tag.find("a")
        if (planetTag is not None) and (planetTag.get_text() not in planetList):
            planetList.append(planetTag.get_text())
        
        if tag.get_text().strip() not in planetList and len(rowList) < 10:
            formattedVal1 = tag.get_text().replace(",", "")
            formattedVal2 = formattedVal1.replace("*", "")
            if (formattedVal2 != "Unknown" and formattedVal2 != "Yes" and formattedVal2 != "No"):
                #If the value is not text based, convert it to a float
                rowList.append(float(formattedVal2))
            elif (formattedVal2 == "Yes" or formattedVal2 == "No"):
                #If the value is a yes or no, simply append that instead of converting to a float and recieving an error
                rowList.append(formattedVal2)
            else:
                #If the value is an unknown, this statement will execute
                rowList.append(np.nan) 
        
    if len(rowList) != 0:
        tableList.append(rowList.copy())
    rowList.clear()
  
counter = 0  
for key in d.keys():
    d[key] = tableList[counter]
    counter += 1
    
d["Planet"] = planetList

df = pd.DataFrame(d)
df.set_index("Planet", inplace = True)

print(df.describe())

df.to_csv("PlanetData.csv", index = False)
