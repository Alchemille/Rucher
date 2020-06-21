mapboxgl.accessToken = 'pk.eyJ1IjoianNvbWEiLCJhIjoibFJmYl9JWSJ9.AUm8d76cbOvVEn2mMeG_ZA';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v10',
    center: [0.529145, 45.440493],
    zoom: 10
});
map.on('load', function () {
    
    var positions = {{ positions | safe }}
    positions.forEach(function (marker) {
    var el = document.createElement('div');
    el.className = 'marker';

    new mapboxgl.Marker(el)
        .setLngLat(marker.geometry.coordinates)
        .setPopup(new mapboxgl.Popup({ offset: [0, -15] }) // add popups
        .setHTML('<h3>' + marker.properties.title + '</h3><p>' + marker.properties.description + '</p>'))
        .addTo(map);
    });
})



