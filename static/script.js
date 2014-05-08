var map;
function initialize() {
  var mapOptions = {
    zoom: 4,
    center: new google.maps.LatLng(40, -3)
  };
  map = new google.maps.Map(document.getElementsByClassName('googleMap-js')[0],
      mapOptions);
}

function addMark() {
	var myLatlng = new google.maps.LatLng(40, -3);

	var marker = new google.maps.Marker({
      position: myLatlng,
      map: map,
      icon:"http://transporte.mincomercio.gob.ve/usuario/imagenes/natural.png",
      title: 'Hola Mundo'
  });
}

//google.maps.event.addDomListener(window, 'load', initialize);
window.onload = initialize;