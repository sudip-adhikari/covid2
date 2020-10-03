# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 12:24:30 2020

@author: Admin
"""

import pandas as pd
import geopandas as gpd


district_dict = {2:'Panchthar',
                 3:'Ilam',
                 4:'Jhapa',
                 5:'Morang',
                 6:'Sunsari',
                 8:'Terhathum',
                 9:'Bhojpur',
                 10:'Sankhuwasabha',
                 11:'Solukhumbu',
                 12:'Khotang',
                 13:'Okhaldhunga',
                 14:'Udayapur',
                 16:'Saptari',
                 20:'Sindhuli',
                 22:'Dolakha',
                 23:'Rasuwa',
                 25:'Nuwakot',
                 28:'Lalitpur',
                 31:'Makawanpur',
                 33:'Bara',
                 34:'Parsa',
                 38:'Kapilbastu',
                 40:'Arghakhanchi',
                 42:'Syangja',
                 44:'Gorkha',
                 46:'Kaski',
                 47:'Manang',
                 50:'Baglung',
                 52:'Dang',
                 54:'Rolpa',
                 58:'Mugu',
                 60:'Jumla',
                 63:'Dailekh',
                 64:'Surkhet',
                 66:'Banke',
                 68:'Doti',
                 70:'Bajura',
                 73:'Baitadi',
                 75:'Kanchanpur',
                 1:'Taplejung',
                 7:'Dhankuta',
                 15:'Siraha',
                 17:'Dhanusha',
                 18:'Mahottari',
                 19:'Sarlahi',
                 21:'Ramechhap',
                 24:'Sindhupalchok',
                 26:'Dhading',
                 27:'Kathmandu',
                 29:'Bhaktapur',
                 30:'Kabhrepalanchok',
                 32:'Rautahat',
                 35:'Chitawan',
                 37:'Rupandehi',
                 39:'Palpa',
                 41:'Gulmi',
                 43:'Tanahu',
                 45:'Lamjung',
                 48:'Mustang',
                 49:'Myagdi',
                 51:'Parbat',
                 53:'Pyuthan',
                 55:'Salyan',
                 57:'Dolpa',
                 59:'Humla',
                 61:'Kalikot',
                 62:'Jajarkot',
                 65:'Bardiya',
                 67:'Kailali',
                 69:'Achham',
                 71:'Bajhang',
                 72:'Darchula',
                 74:'Dadeldhura',
                 481:'Nawalparasi East',
                 482:'Nawalparasi West',
                 541:'Rukum East',
                 542:'Rukum West'}

province = {1:'1',
            2:'2',
            3:'Bagmati',
            4:'Gandaki',
            5:'5',
            6:'Karnali',
            7:'Sudur Paschim'}


#Loading Map of nepal with district divison
map_district = gpd.read_file(r'H:\projects\gis\npl_admbnda_nd_20190430_shp\npl_admbnda_districts_nd_20190430.shp')
map_district = map_district[['DIST_EN','geometry']]

#Loading map of Nepal with local units
map_nep = gpd.read_file(r'H:\mausam\python  ex\covid-19\nepal administ\Local Unit\local_unit.shp')
map_nep = map_nep[['Province','DISTRICT','GaPa_NaPa','geometry']]

#Extracting the geometry of Byas  Gaupalika in Darchulla district
count = 0
for district, local in zip(map_nep['DISTRICT'],map_nep['GaPa_NaPa']):
    if district == 'DARCHULA' and local == 'Byas':       
        byas_geo = map_nep['geometry'][count]
        #print(byas_geo)
    count += 1

#Appending the new Byas Gauplika 
new_map = map_district.copy()
new_map.loc[77] = ['Darchula',byas_geo]
new_map = new_map[['DIST_EN','geometry']]
new_map.rename(columns={'DIST_EN':'DISTRICT'}, inplace=True)




#Data Preprocessing
districts = pd.read_csv('H:\mausam\python  ex\covid-19\csv data\district_list.csv',index_col=0)

covid_cases = pd.read_csv('H:\mausam\python  ex\covid-19\csv data\sep21_active_district.csv')
covid_cases = covid_cases[['DISTRICT_id','Active']]


values = covid_cases['DISTRICT_id'].tolist()
values_case = covid_cases['Active'].tolist()
new_values = []
for value, d_val in zip(values,values_case):
    new_values.append((district_dict[value], value, d_val ))
    
covid_cases = pd.DataFrame(columns={'DISTRICT','DISTRICT_id','Active'}, data=new_values)
covid_cases = covid_cases.set_index('DISTRICT_id')


districts = districts.join(covid_cases['Active'], on='DISTRICT_id', rsuffix='Active')
districts = districts.reset_index(drop=True)

#filling nan values with 0
districts['Active'] = districts['Active'].fillna(0)


new_map = new_map[['DISTRICT','geometry']]
#districts = districts[['DISTRICT','Active']]
new_map = new_map.merge(districts, on='DISTRICT')
new_map.plot(column='Active',figsize=(10,8),cmap='nipy_spectral',legend=True)



















