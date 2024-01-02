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
from pg.pg import Pg

# initializing the database and geoserver
db = Pg(dbname='geoapp', user='kate', password='cateobi',host='localhost', port='5432')
geo = Geoserver('http://localhost:8080/geoserver', username='admin', password='geoserver')
conn_str = 'postgresql://kate:cateobi@localhost:5432/geoapp'

# Create your models here.
class landmarks(models.Model):
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length=1000, blank=True)
    file = models.FileField(upload_to='%y/%m/%d')
    uploaded_date = models.DateField(default= datetime.date.today, blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'landmark'
        verbose_name_plural = 'landmarks'

# save posted shpapefile
@receiver(post_save, sender=landmarks)
def publish_data(sender, instance, created, **kwargs):
    file = instance.file.path
    file_format = os.path.basename(file).split('.')[-1]
    file_name = os.path.basename(file).split('.')[0]
    file_path = os.path.dirname(file)
    name = instance.name

    # extract zipfile
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(file_path)

    os.remove(file)  # remove zip file

    shp = glob.glob(r'{}/**/*.shp'.format(file_path),
                    recursive=True)  # to get shp
    try:
        req_shp = shp[0]
        gdf = gpd.read_file(req_shp)  # make geodataframe
        engine = create_engine(conn_str)
        gdf.to_postgis(
            con=engine,
            schema='data',
            name=name,
            if_exists="replace")

        for s in shp:
            os.remove(s)

    except Exception as e:
        for s in shp:
            os.remove(s)

        instance.delete()
        print("There is problem during shp upload: ", e)

    # publish shp to the geoserver using geoserver-rest
    #geo.create_workspace(workspace='geoapp')

    geo.create_featurestore(store_name='geoApp', workspace='geoapp', db='geoapp', host='localhost', pg_user='kate', pg_password='cateobi', schema='data')
    
    geo.publish_featurestore(workspace='geoapp', store_name='geoApp', pg_table=name)

    geo.create_outline_featurestyle('geoapp_shp', workspace='geoapp')

    geo.publish_style(layer_name=name, style_name='geoapp_shp', workspace='geoapp')

# delete posted shpapefile
@receiver(post_delete, sender=landmarks)
def delete_data(sender, instance, **kwargs):
    db.delete_table(instance.name, schema='data')
    geo.delete_layer(instance.name, 'geoapp')