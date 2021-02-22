var lat = document.getElementById("latitude").value;
lat=parseFloat(lat);

var lon = document.getElementById("longitude").value;
lon=parseFloat(lon);

function directions(){
    var H;
    var V;

    if(lat<0){
        H = 'S'
    }else{
        H = 'N'
    }

    if(lon<0){
        V = 'W'
    }else{
        v = 'E'
    }
    document.getElementById('latitude').innerHTML = H;
    document.getElementById('longitude').innerHTML = V;
}
window.onload = directions;
