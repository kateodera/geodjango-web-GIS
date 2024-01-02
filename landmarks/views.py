from django.shortcuts import render
from .models import landmarks
from baselayer.models import tiff

# Create your views here.
def index(request):
    shp = landmarks.objects.all()
    tif = tiff.objects.all()
    return render(request,'index.html', {'shp':shp,'tiff':tif})





