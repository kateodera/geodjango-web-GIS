// map class initialize
var map = L.map('map').setView([1.2921, 36.8219], 7);    map.zoomControl.setPosition('topright');

// adding osm tile
var osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

//cartodb tile
var DarkMatter = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 20
});

// usgimagery topo
var USImageryTopo = L.tileLayer('https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryTopo/MapServer/tile/{z}/{y}/{x}', {
maxZoom: 20,
attribution: 'Tiles courtesy of the <a href="https://usgs.gov/">U.S. Geological Survey</a>'
});


// add map scale
L.control.scale({position: "bottomleft"}).addTo(map);

//map coordinate
map.on('mousemove',function(e){
    $('.coordinate').html(`Lat:${e.latlng.lat} Lon: ${e.latlng.lng}`)
});

// map cluster
var marker = L.markerClusterGroup();
var clust = L.geoJSON(data,{
    onEachFeature: function(feature, layer){
        layer.bindPopup(feature.properties.name)
    }

});

clust.addTo(marker)
marker.addTo(map)

//Leaflet layer control
var baseMaps ={
    'OSM':osm,
    'Carto':DarkMatter,
    'topo':USImageryTopo
}



