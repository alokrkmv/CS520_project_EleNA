var routeInMarkers = []

$(document).ready(function(){
    $('#submitform').click(function(e) {
        validateForm()
        document.getElementById("map").style.display = 'block';
        document.getElementById("map").style.visibility = 'hidden';
        document.getElementById("loader").style.display = 'block';
        document.getElementById("res").innerHTML = '';
        routeInMarkers = []
        var ReceivedJSON = (FormDataToJSON(document.getElementById("myform")));
        delete ReceivedJSON['txtMsg'];
        var jsonObj = {};
        jsonObj.data = ReceivedJSON;
        console.log(JSON.stringify(jsonObj));
        fetch("http://localhost:8000/fetch_route", {
            method: "POST",
            body: JSON.stringify(jsonObj),
            headers: {
            "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(response => {
            if (response.hasOwnProperty('message')) {
              document.getElementById("map").style.display = 'none';
              document.getElementById("loader").style.display = 'none';
              console.log(response.message)
              document.getElementById("res").innerHTML = '<span style="color: #C41E3A">' + response.message;
            } else {
                for (let item of response.route) {
                  temp = {}
                  temp['latitude'] = item[0].toString()
                  temp['longitude'] = item[1].toString()
                  routeInMarkers.push(temp)
                }
                console.log(routeInMarkers)
                initMap(response.source, response.destination, routeInMarkers)
                document.getElementById("res").innerHTML = 'Yay! Route found with with distance <span style="color: #48aaad">' + response.distance
                    + '</span> and elevation gain <span style="color: #48aaad">' + response.elevation_gain + '</span>'
            }
         })
        .catch();
        e.preventDefault(); //STOP default action
    });
  });

function validateForm() {
    var a = document.forms["myform"]["autocomplete_source"].value;
    var b = document.forms["myform"]["autocomplete_dest"].value;
    if (a == null || a == "", b == null || b == "") {
        alert("Please Fill All Required Fields");
    return false;
    }
}


function FormDataToJSON(FormElement){
    var formData = new FormData(FormElement);
    var ConvertedJSON= {};
    for (const [key, value]  of formData.entries())
    {
        ConvertedJSON[key] = value;
    }
    return ConvertedJSON
}

function initMap(source, destination, markers) {
        source = new google.maps.LatLng(source[0], source[1])
        destination = new google.maps.LatLng(destination[0], destination[1])

        var mapOptions = {
            center: new google.maps.LatLng(markers[~~(markers.length/2)]['latitude'], markers[~~(markers.length/2)]['longitude']),
            zoom: 13,
            mapTypeId: google.maps.MapTypeId.ROADMAP
         };

        var pinSVGFilled = "M 12,2 C 8.1340068,2 5,5.1340068 5,9 c 0,5.25 7,13 7,13 0,0 7,-7.75 7,-13 0,-3.8659932 -3.134007,-7 -7,-7 z";
        var pinColor = "#48aaad";
        var labelOriginFilled =  new google.maps.Point(12,9);
        var pinLabel = "A";

        var markerImage = {
            path: pinSVGFilled,
            anchor: new google.maps.Point(12,17),
            fillOpacity: 1,
            fillColor: pinColor,
            strokeWeight: 2,
            strokeColor: "white",
            scale: 2,
            labelOrigin: labelOriginFilled
        };
        var label = {
            text: pinLabel,
            color: "white",
            fontSize: "12px",
        };
        var map = new google.maps.Map(document.getElementById("map"), mapOptions);
        var directionsService = new google.maps.DirectionsService();
        var directionsDisplay = new google.maps.DirectionsRenderer();// also, constructor can get "DirectionsRendererOptions" object
        directionsDisplay.setMap(map);

        var waypoints = [];

        marker = new google.maps.Marker({
                position: source,
                map: map,
                label: 'Source',
                icon: markerImage
        });
        marker = new google.maps.Marker({
                position: destination,
                map: map,
                label: 'Destination',
                icon: markerImage
        });

        for (var i = 0; i < markers.length; i++) {
            temp = new google.maps.LatLng(markers[i].latitude, markers[i].longitude)
            waypoints.push({location: temp, stopover: false});
        }
         calculateAndDisplayRoute(directionsService, directionsDisplay, source, destination, waypoints);
}

function calculateAndDisplayRoute(directionsService, directionsDisplay, source, destination, waypoints) {
      directionsService.route({
        origin: source,
        destination: destination,
        waypoints: waypoints,
        travelMode: google.maps.TravelMode.WALKING
      }, function(response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
          directionsDisplay.setDirections(response);
        } else {
            directionsService.route({
                origin: source,
                destination: destination,
                waypoints: waypoints,
                travelMode: google.maps.TravelMode.DRIVING
              }, function(response, status) {
                    if (status == google.maps.DirectionsStatus.OK) {
                      directionsDisplay.setDirections(response);
                    } else {
                      window.alert('Directions request failed due to ' + status);
                      document.getElementById("res").innerHTML = '<span style="color: #C41E3A"> No Route Found';
                    }
                }
              );
            }
      });
      document.getElementById("loader").style.display = 'none';
      document.getElementById("map").style.visibility = 'visible';
}

