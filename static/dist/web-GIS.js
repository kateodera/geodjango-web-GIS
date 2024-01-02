// full screen map view
var mapId =document.getElementById('map');
function fullScreenView(){
    if (document.fullscreenElement){
        document.exitFullscreen();
    }else{
    mapId.requestFullscreen();
    }
};

//browser print function
L.control.browserPrint({position:'topright'}).addTo(map);


// map geocoder search
L.Control.geocoder().addTo(map);

// zoom to layer
$('.zoom-to-layer').click(function(){
    map.setView([1.2921, 36.8219], 7)
})

//Leaflet measure
L.control.measure({
    primaryLengthUnit: 'kilometer', 
    secondaryLengthUnit: 'meter',
    primaryAreaUnit: 'sqmeters', 
    secondaryAreaUnit: undefined 
}
).addTo(map);
