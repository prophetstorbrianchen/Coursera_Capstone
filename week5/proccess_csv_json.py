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
        #self.address = "C:\\Users\\Brian\\Desktop\\ibm_coursera\\Coursera_Capstone\week4\\"
        self.address = "C:\\Users\\brian\\Desktop\\Coursera_Capstone\\week4\\"
    
    def load_from_csv(self, filename):
        df = pd.read_csv(self.address + filename, encoding='UTF-8')
        return df
    
    def write_to_csv(self, filename, dictionary):
        colume_list = []
        
        for key, value in dictionary.items():
            colume_list.append(key)
        
        df = pd.DataFrame(dictionary, columns=colume_list)
        df.to_csv(self.address + filename, index=False, encoding="utf_8_sig")

    
class JsonProcess(object):
    
    def __init__(self):
        #self.address = "C:\\Users\\Brian\\Desktop\\ibm_coursera\\Coursera_Capstone\week4\\"
        self.address = "C:\\Users\\brian\\Desktop\\Coursera_Capstone\\week4\\"
    
    def load_from_json(self, filename):
        json_file = open(self.address + filename, "r", encoding="utf-8")
        j = json_file.read()
        json_file.close()
        dict_data = json.loads(j)
        return dict_data
    
    def dictionary_to_json(self, dictionary):
        json_data = json.dumps(dictionary)
        return json_data
    

class GetDateFromWeb(object):
    
    def get_taichung_info(self):
        response = requests.get('https://zh.wikipedia.org/wiki/臺中市#人口')
        content = response.content
        df = pd.read_html(content, encoding='utf-8')
        taichung_info_df = df[11]
        
        return taichung_info_df
        
    
class DataProcess(object):
    
    def __init__(self):
        pass
    
    def merge_dataframe(self, source_df, target_df, field_name):
        df = pd.merge(source_df, target_df, on=field_name)
        return df
    
    def drop_rename_dataframe(self, df, row_drop_list, colume_drop_list, rename_list):
        df = df.drop(row_drop_list)
        df = df.drop(columns=colume_drop_list)
        for item in rename_list:
            for key, value in item.items():    
                df = df.rename(columns={key: value})
                
        return df

    
if __name__ == "__main__":
    
    csvProcess = CSVprocess()
    jsonProcess = JsonProcess()
    dataProcess = DataProcess()
    getDataFromWeb = GetDateFromWeb()
    
    # Get dataframe from Wiki
    row_drop_list = [29]
    colume_drop_list = ["下轄里數", "下轄鄰數", "人口消長", "地理分區"]
    rename_list = [{"區名": "Chinese Name"},{"面積（km²）": "Area"},{"人口數": "Population"},{"人口密度（人/km²）": "Density"},{"郵遞區號": "Postal Code"}]
    
    df = getDataFromWeb.get_taichung_info()
    df = dataProcess.drop_rename_dataframe(df, row_drop_list, colume_drop_list, rename_list)
    csvProcess.write_to_csv("Taichung_info_temp.csv", df.to_dict())
    
    # Load Taichung Dataframe from csv file
    taichung_df = csvProcess.load_from_csv("Taichung_info_temp.csv")
    taichung_english_name_df = csvProcess.load_from_csv("Taichung_English_Name.csv")
    
    # Load Taiwan Geospatial Coordinates from json file
    taiwan_geo_dict = jsonProcess.load_from_json("Taiwan_Geospatial_Coordinates.json")
    
    # Merge Chinese Name and English Name on Taiwan location
    temp_df = dataProcess.merge_dataframe(taichung_df, taichung_english_name_df, "Chinese Name")
    
    # Merge the Latitude and Longitude with taichung info
    temp_df = pd.concat([temp_df, pd.DataFrame(columns=['Latitude', 'Longitude'])], sort=False)
    
    # Merge Taichung Info and Taiwan Geospatial Coordinates
    for i, item in enumerate(temp_df["Postal Code"]):
        for info in taiwan_geo_dict["dataroot"]["_x0031_050429_行政區經緯度_x0028_toPost_x0029_"]:
            postal_code = int(info["_x0033_碼郵遞區號"])
            latitude = float(info["中心點緯度"])
            longitude = float(info["中心點經度"])
            if int(item) == int(postal_code):
                temp_df["Latitude"][i] = latitude
                temp_df["Longitude"][i] = longitude

    # Write to csv file
    temp_df.to_dict()
    csvProcess.write_to_csv("Taichung_Merge_Info_temp.csv", temp_df.to_dict())


    """
    # for test
    dict_data = {}
    json_data = jsonProcess.dictionary_to_json(dict_data)
    print(json_data)
    """
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    