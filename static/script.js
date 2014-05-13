var map;
function initialize() {
  var mapOptions = {
    zoom: 4,
    center: new google.maps.LatLng(40, -3)
  };
  map = new google.maps.Map(document.getElementsByClassName('googleMap-js')[0],
      mapOptions);
}

function putMark(la, lo, pic, name){
  console.log(la + " - " + lo);
  var myLatlng = new google.maps.LatLng(la, lo);
  var marker = new google.maps.Marker({
      position: myLatlng,
      map: map,
      icon: pic,
      title: name
  });
}

function addMark() {
  lista = document.getElementsByClassName('friends_list-js')[0].getElementsByTagName('li');
  for (var i = 0, n = lista.length; i < n; i++) {
    j = 0;
    z = 0;
    //Search id of the friend
    while (friends[j].id != lista[i].id) {
      j++;
    }
    //Search coordinates
    while (friends[j].hometown != locations[z].id) {
      z++;
    }

    putMark(locations[z].latitude, locations[z].longitude, friends[j].picture, friends[j].name);

  }
}

//google.maps.event.addDomListener(window, 'load', initialize);
window.onload = initialize;