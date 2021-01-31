import pandas as pd 
import satelliteimage as si 


citydf = pd.read_csv("/content/gdrive/MyDrive/images_satellite/Nigeria.csv")
yrdata = pd.read_csv("/content/gdrive/MyDrive/images_satellite/yrdata_range.csv")
yrdata = yrdata[yrdata['year']>=1996].reset_index(drop = True) ## since night light images are only available from 1996
for city in citydf['name'].unique()[:5]:
    print(city)
    lat = float(citydf[citydf['name']==city]['lat'].unique()[0])
    lon = citydf[citydf['name']==city]['lon'].unique()[0]
    for i in range(len(yrdata)):
        print(i)
        year = yrdata['year'][i]
        start_date = yrdata['start_date'][i]
        end_date = yrdata['end_date'][i]
        print(start_date,end_date)
        nightlightimg = si.nightlightimages(city,start_date,end_date,year,lat,lon)
        nightlightimg.getgeometry()
        img_col = nightlightimg.nightlightdata()
        nightlightimg.saveimages()
