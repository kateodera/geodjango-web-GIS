from django.db import models
import datetime
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
import geopandas as gpd
import os
import glob
import zipfile
from sqlalchemy import *
from geo.Geoserver import Geoserver

# initializing the database and geoserver
geo = Geoserver('http://localhost:8080/geoserver', username='admin', password='geoserver')

# Create your models here.
class tiff(models.Model):
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length=1000, blank=True)
    file = models.FileField(upload_to='%y/%m/%d')
    uploaded_date = models.DateField(default= datetime.date.today, blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'tiff'
        verbose_name_plural = 'tiffs'


# save posted tiff
@receiver(post_save, sender=tiff)
def publish_data(sender, instance, created, **kwargs):
    file = instance.file.path
    file_format = os.path.basename(file).split('.')[-1]
    file_name = os.path.basename(file).split('.')[0]
    file_path = os.path.dirname(file)
    name = instance.name


    # publish tiff to the geoserver using geoserver-rest
    geo.create_coveragestore(file, workspace='geoapp', layer_name=name)
    geo.create_coveragestyle(file, style_name=name, workspace='geoapp')
    #geo.publish_style(layer_name=name, style_name=name, workspace='geoapp')
    

# delete posted shpapefile
@receiver(post_delete, sender=tiff)
def delete_data(sender, instance, **kwargs):
    geo.delete_layer(instance.name, 'geoapp')