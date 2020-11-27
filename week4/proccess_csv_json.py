import pandas as pd
import numpy as np
import json
import requests
import os
from sklearn.cluster import KMeans
import folium # map rendering library
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
import matplotlib.cm as cm
import matplotlib.colors as colors
from bs4 import BeautifulSoup
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe


class CSVprocess(object):
    
    def __init__(self):
        self.address = "C:\\Users\\Brian\\Desktop\\ibm_coursera\\Coursera_Capstone\week4\\"
    
    def load_from_csv(self, filename):
        df = pd.read_csv(self.address + filename, encoding='UTF-8')
        return df
    
    def write_to_csv(self, filename, dictionary):
        colume_list = []
        
        for key, value in dictionary.items():
            colume_list.append(key)
        
        df = pd.DataFrame(dictionary, columns=colume_list)
        df.to_csv(self.address + filename, index=False, encoding="utf_8_sig")
    
    def merge_dataframe(self, source_df, target_df, field_name):
        df = pd.merge(source_df, target_df, on=field_name)
        return df
    
class JsonProcess(object):
    
    def __init__(self):
        self.address = "C:\\Users\\Brian\\Desktop\\ibm_coursera\\Coursera_Capstone\week4\\"
    
    def load_from_json(self, filename):
        json_file = open(self.address + filename, "r", encoding="utf-8")
        j = json_file.read()
        json_file.close()
        dict_data = json.loads(j)
        return dict_data
    

if __name__ == "__main__":
    
    csvProcess = CSVprocess()
    jsonProcess = JsonProcess()
    taichung_df = csvProcess.load_from_csv("Taichung_info.csv")
    taichung_english_name_df = csvProcess.load_from_csv("Taichung_English_Name.csv")
    temp_df = csvProcess.merge_dataframe(taichung_df, taichung_english_name_df, "Chinese Name")
    temp_df = pd.concat([temp_df, pd.DataFrame(columns=['Latitude', 'Longitude'])], sort=False)

    taiwan_geo_dict = jsonProcess.load_from_json("Taiwan_Geospatial_Coordinates.json")
    
    for i, item in enumerate(temp_df["Postal Code"]):
        for info in taiwan_geo_dict["dataroot"]["_x0031_050429_行政區經緯度_x0028_toPost_x0029_"]:
            postal_code = int(info["_x0033_碼郵遞區號"])
            latitude = float(info["中心點緯度"])
            longitude = float(info["中心點經度"])
            if int(item) == int(postal_code):
                temp_df["Latitude"][i] = latitude
                temp_df["Longitude"][i] = longitude

    temp_df.to_dict()
    csvProcess.write_to_csv("Taichung_Merge_Info.csv", temp_df.to_dict())

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    