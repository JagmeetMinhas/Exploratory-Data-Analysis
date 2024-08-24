#Import libraries
import requests
import json
import pandas as pd

#Create lists for each column of data 
speedList = []
halfAngleList = []
latitudeList = []
longitudeList = []
notesList = []

#Initalize an API key string and endpoint f string to insert the API key
apiKey = "REDACTED"
url = f"https://api.nasa.gov/DONKI/CMEAnalysis?startDate=2016-09-01&endDate=2017-09-30&mostAccurateOnly=true&catalog=ALL&api_key={apiKey}"

#Make a request to the endpoint
apiCall = requests.get(url)

#If the request is successful, proceed with scraping
if (apiCall.status_code == 200):
    
    #Recieve the JSON from the API request and format it (not necessary but helps for viewing purposes)
    rawJSON = apiCall.json()
    formattedJSON = json.dumps(rawJSON, sort_keys = True, indent = 4)
    
    #Iterate through each entry in the JSON and extract the pertient data, appending to the appropriate list
    for cme in rawJSON:
        speedList.append(cme["speed"])
        halfAngleList.append(cme["halfAngle"])
        latitudeList.append(cme["latitude"])
        longitudeList.append(cme["longitude"])
        notesList.append(cme["note"])
    
    #Append all of the lists into a dictionary
    d = {"Speed (km/s)": speedList, 
         "Half Angle (radians)": halfAngleList,
         "Latitude (degrees)": latitudeList,
         "Longitude (degrees)": longitudeList,
         "Note": notesList}
    
    #Create a dataframe
    df = pd.DataFrame(d)
        
    #Generate summary statistics
    print(df.describe())
    
    #Export to CSV
    df.to_csv("CMEData.csv", index = False)
