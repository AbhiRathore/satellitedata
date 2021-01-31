import time

import ee
import logging

import json
import os
from functools import partial
ee.Initialize()

import pyproj
from shapely.geometry import Point, mapping
from shapely.ops import transform
from tqdm import tqdm
from shapely.geometry import shape
# create logger 
logger = logging.getLogger('twitter_scrapper')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('tweetScrap.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


def buffer_extent(lat, lon, dst_epsg, buffer_size):
    """Generate a buffer around a location and returns
    the geometry corresponding to its spatial envelope.
    """
    center = reproject_geom(
        Point(lon, lat), src_epsg=4326, dst_epsg=dst_epsg)
    buffer = center.buffer(buffer_size)
    return buffer.exterior.envelope


def reproject_geom(geom, src_epsg, dst_epsg):
    """Reproject a shapely geometry given a source EPSG and a
    target EPSG.
    """
    src_proj = pyproj.Proj(init='epsg:{}'.format(src_epsg))
    dst_proj = pyproj.Proj(init='epsg:{}'.format(dst_epsg))
    reproj = partial(pyproj.transform, src_proj, dst_proj)
    return transform(reproj, geom)

def geojson_crs(epsg):
    """Generate a GeoJSON CRS member from an EPSG code."""
    epsg = int(epsg)
    if epsg == 4326:
        coordinate_order = [1, 0]
    else:
        coordinate_order = [0, 1]
    return {
        'type': 'EPSG',
        'properties': {'code': epsg, 'coordinate_order': coordinate_order}}

def as_geojson(geom, epsg=None):
    """Get a GeoJSON-like dictionnary of a single shapely geometry."""
    geojson = {'type': 'Feature', 'geometry': mapping(geom)}
    if epsg:
        geojson.update(crs=geojson_crs(epsg))
    return geojson

class nightlightimages:
    def __init__(self,city,startdate,enddate,year,lat,lon):
        self.city = city 
        self.startdate = startdate
        self.enddate = enddate
        self.year = year
        self.lat = lat 
        self.lon = lon 


    def getgeometry(self):
        self.extent = buffer_extent(self.lat, self.lon, 3857 , buffer_size=20000) #1.6594, 28.0339
        self.extent = as_geojson(self.extent,3857 )
        self.aoi = reproject_geom(shape(self.extent['geometry']), 3857, 4326)
        self.xmin, self.ymin, self.xmax, self.ymax = [round(coord, 3) for coord in self.aoi.bounds]
        self.bbox = [self.xmin, self.ymin, self.xmax, self.ymax]
        self.geom = ee.Geometry.Rectangle(self.bbox)
        return self.geom

    def nightlightdata(self):
        #self.geom = getgeometry()

        if self.year <= 2011:
            self.img_col = ee.ImageCollection('NOAA/DMSP-OLS/CALIBRATED_LIGHTS_V4').filter(ee.Filter.date(self.startdate, self.enddate)).select('cf_cvg').mosaic()
        else:
            self.img_col = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG').filter(ee.Filter.date(self.startdate, self.enddate)).median().select([0], ['NIGHTLIGHTS'])

        return self.img_col

    def saveimages(self):
        self.task_config = {
            'description': self.city + "_images_" + str(self.year),
            'scale': 30,
            'folder': 'images_satellite_' + self.city,
            'fileNamePrefix':self.city + "_images_" + str(self.year),
            'region':  self.geom.getInfo()['coordinates'] 
        }
        self.task = ee.batch.Export.image.toDrive(image=self.img_col,**self.task_config)
        self.task.start()
        
        
        erflag = 0
        while self.task.status()['state'] != 'COMPLETED':   
            print(f">>task status: {self.task.status()['state']}")
            time.sleep(3)
            if self.task.status()['state'] == 'FAILED':
                erflag = 1
                break

        if erflag ==0:
            print("completed for {} city and {} year".format(self.city,self.year))
            logger.info("completed for {} city and {} year".format(self.city,self.year))
        elif erflag == 1:
            print("errored out for {} city and {} year".format(self.city,self.year))
            logger.info("errored out for {} city and {} year".format(self.city,self.year))

        
        return("completed")
        

