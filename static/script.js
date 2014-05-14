var map;
var markers = [];

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
  markers.push(marker);
}

// Sets the map on all markers in the array.
function setAllMap(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
  setAllMap(null);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
  clearMarkers();
  markers = [];
}


function addMark() {
  deleteMarkers();
  select = document.getElementsByClassName("select-js")[0];
  search = select.options[select.selectedIndex].value;

  lista = document.getElementsByClassName('friends_list-js')[0].getElementsByTagName('li');
  for (var i = 0, n = lista.length; i < n; i++) {
    j = 0;
    z = 0;
    //Search id of the friend
    while (friends[j].id != lista[i].id) {
      j++;
    }
    //Search coordinates
    if (search == "Nacimiento") {
      if (friends[j].hometown != "None") {
        while (friends[j].hometown != locations[z].id) {
          z++;
        }
        putMark(locations[z].latitude, locations[z].longitude, friends[j].picture, friends[j].name);
      }
    } else {
      if (friends[j].location != "None") {
        while (friends[j].location != locations[z].id) {
          z++;
        }
        putMark(locations[z].latitude, locations[z].longitude, friends[j].picture, friends[j].name);
      }
    }
   
    

  }
}

//google.maps.event.addDomListener(window, 'load', initialize);
window.onload = initialize;