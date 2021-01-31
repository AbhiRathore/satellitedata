import pandas as pd 
import satelliteimage as si 
import os 
#citydf = pd.read_csv("/content/gdrive/MyDrive/images_satellite/rwandadata.csv")
citydf_total = pd.read_csv("/content/gdrive/MyDrive/images_satellite/nigeriasurveyelectricity.csv")
country = 'nigeria'

alreadydone = [int(j.split('nigeria_cluster_')[1]) for j in os.listdir("/content/gdrive/MyDrive/") if country in j and 'satellite' in j]
# print(alreadydone)

citydf = citydf_total[~citydf_total['cluster'].isin(alreadydone)]

print(len(citydf),len(citydf_total))

yrdata = pd.read_csv("/content/gdrive/MyDrive/images_satellite/yrdata_range.csv")
yrdata = yrdata[yrdata['year']>=1996].reset_index(drop = True) ## since night light images are only available from 1996
for city in citydf['cluster'].unique():
    print(city)
    lat = float(citydf[citydf['cluster']==city]['latitude'].unique()[0])
    lon = citydf[citydf['cluster']==city]['longitude'].unique()[0]
    start_date = '2018-1-1'
    end_date = '2018-12-31'
    print(start_date,end_date)
    city = "cluster_" + str(city)
    year = 2018
    nightlightimg = si.nightlightimages(city,country,start_date,end_date,year,lat,lon)
    nightlightimg.getgeometry()
    img_col = nightlightimg.nightlightdata()
    nightlightimg.saveimages()






    # for i in range(len(yrdata)):
    #     print(i)
    #     year = yrdata['year'][i]
    #     start_date = yrdata['start_date'][i]
    #     end_date = yrdata['end_date'][i]
    #     print(start_date,end_date)
    #     nightlightimg = si.nightlightimages(city,start_date,end_date,year,lat,lon)
    #     nightlightimg.getgeometry()
    #     img_col = nightlightimg.nightlightdata()
    #     nightlightimg.saveimages()
