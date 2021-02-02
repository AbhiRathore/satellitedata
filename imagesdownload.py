import pandas as pd 
import satelliteimages as si 
import os 
country = 'berundi'



#citydf = pd.read_csv("/content/gdrive/MyDrive/images_satellite/rwandadata.csv")
imgdir = "/content/gdrive/MyDrive/satellite_image_datafiles/"

shapefilename =country + "shapefile.csv"
citydf_total = pd.read_csv("/content/gdrive/MyDrive/dataAfrica/" + shapefilename)

citydf_total.columns = ['cluster','latitude','longitude']

# alreadydone = [int(j.split('berundi_')[1].split("_")[0]) for j in os.listdir(imgdir) if country in j and '.tif' in j]
# print(alreadydone)

## to obtain already done cluster id 
alreadydone = [int(j.split(country + "_")[1].split("_")[0]) for j in os.listdir(imgdir) if country in j and '.tif' in j]



citydf = citydf_total[~citydf_total['cluster'].isin(alreadydone)]

print(len(citydf),len(citydf_total))

for city in citydf['cluster'].unique():
    print(city)
    lat = float(citydf[citydf['cluster']==city]['latitude'].unique()[0])
    lon = citydf[citydf['cluster']==city]['longitude'].unique()[0]
    start_date = '2016-1-1'
    end_date = '2017-12-31'
    print(start_date,end_date)
    city = "cluster_" + str(city)
    year = 2016
    nightlightimg = si.nightlightimages(city,country,start_date,end_date,year,lat,lon)
    nightlightimg.getgeometry()
    img_col = nightlightimg.nightlightdata()
    nightlightimg.saveimages()




