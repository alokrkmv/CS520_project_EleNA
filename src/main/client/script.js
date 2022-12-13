var routeInMarkers = []

$(document).ready(function(){
    $('#submitform').click(function(e) {
        document.getElementById("map").style.visibility = 'visible';
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
            console.log(response);
            for (let item of response.route) {
              temp = {}
              temp['latitude'] = item[0].toString()
              temp['longitude'] = item[1].toString()
              routeInMarkers.push(temp)
            }
            console.log(routeInMarkers)
            initMap(routeInMarkers)
            document.getElementById("res").innerHTML = 'Yay! Route found with with distance <span style="color: #48aaad">' + response.distance
                + '</span> and elevation gain <span style="color: #48aaad">' + response.elevation_gain + '</span>'
         })
        .catch();
        e.preventDefault(); //STOP default action
    });
  });


function FormDataToJSON(FormElement){
    var formData = new FormData(FormElement);
    var ConvertedJSON= {};
    for (const [key, value]  of formData.entries())
    {
        ConvertedJSON[key] = value;
    }
    return ConvertedJSON
}

function initMap(markers) {
//     console.log(markers)
//      var mapOptions = {
//        center: new google.maps.LatLng(markers[~~(markers.length/2)]['latitude'], markers[~~(markers.length/2)]['longitude']),
//        zoom: 13,
//        mapTypeId: google.maps.MapTypeId.ROADMAP
//      };
//      var map = new google.maps.Map(document.getElementById("map"), mapOptions);
//      var positions = [];
//      var icon;
//      var marker;
//      for (var i = 0; i < markers.length; i++) {
//          positions.push(new google.maps.LatLng(markers[i].latitude, markers[i].longitude))
//          if (i == 0 || i == markers.length - 1) {
//                marker = new google.maps.Marker({
//                    position: positions[i],
//                    map: map,
//                    title: 'Click me'
//                });
//            } else {
//                marker = new google.maps.Marker({
//                    position: positions[i],
//                    map: map,
//                    icon: {
//                        path: google.maps.SymbolPath.CIRCLE,
//                        scale: 0
//                    },
//                    title: 'Click me'
//                });
//            }
//        }
//
//        //Intialize the Path Array
//        var path = new google.maps.MVCArray();
//        //Intialize the Direction Service
//        var service = new google.maps.DirectionsService();
//        var flightPath = new google.maps.Polyline({
//          path: positions,
//          geodesic: true,
//          strokeColor: '#4986E7'
//        });
//        flightPath.setMap(map);


        var mapOptions = {
        center: new google.maps.LatLng(markers[~~(markers.length/2)]['latitude'], markers[~~(markers.length/2)]['longitude']),
        zoom: 13,
        mapTypeId: google.maps.MapTypeId.ROADMAP
         };
        var map = new google.maps.Map(document.getElementById("map"), mapOptions);
        var directionsDisplay;
        var directionsService = new google.maps.DirectionsService();

        directionsDisplay = new google.maps.DirectionsRenderer();
        directionsDisplay.setMap(map);


        var startPoint;
        var endPoint;
        var waypts = [];

        var infowindow = new google.maps.InfoWindow();
        var i;

        for (i = 0; i < markers.length; i++) {
            if (i == 0 || i == markers.length - 1) {
                marker = new google.maps.Marker({
                position: new google.maps.LatLng(markers[i].latitude, markers[i].longitude),
                map: map,
                label: markers[i].count
                });
            }
            waypts.push(new google.maps.LatLng(markers[i].latitude, markers[i].longitude))
        }


        for (var i = 0, parts = [], max = 8 - 1; i < waypts.length; i = i + max)
            parts.push(waypts.slice(i, i + max + 1));

        // Callback function to process service results
        var service_callback = function(response, status) {
            if (status != 'OK') {
                console.log('Directions request failed due to ' + status);
                return;
            }
            var renderer = new google.maps.DirectionsRenderer;
            renderer.setMap(map);
            renderer.setOptions({ suppressMarkers: true, preserveViewport: true });
            renderer.setDirections(response);
        };

        // Send requests to service to get route (for stations count <= 25 only one request will be sent)
        for (var i = 0; i < parts.length; i++) {
            // Waypoints does not include first station (origin) and last station (destination)
            var waypoints = [];
            for (var j = 1; j < parts[i].length - 1; j++)
                waypoints.push({location: parts[i][j], stopover: false});
            // Service options
            var service_options = {
                origin: parts[i][0],
                destination: parts[i][parts[i].length - 1],
                waypoints: waypoints,
                travelMode: 'WALKING'
            };
            // Send request
            directionsService.route(service_options, service_callback);
        }
//
//        google.maps.event.addListener(marker, 'click', (function(marker, i) {
//            return function() {
//                infowindow.setContent("Name :"+markers[i].name+","+"<br>"+"Date & Time :"+markers[i].date+", "+markers[i].time+","+"<br>"+"Location :"+markers[i].address);
//                infowindow.open(map, marker);
//            }
//        })(marker, i));
//        }
//        calcRoute(startPoint, endPoint, waypts);
//        //add this function
//        function calcRoute(start,end,waypts) {
//            var request = {
//                origin: start,
//                destination: end,
//                waypoints: waypts,
//                travelMode: google.maps.DirectionsTravelMode.DRIVING
//            };
//            directionsService.route(request, function(response, status) {
//            if (status == google.maps.DirectionsStatus.OK) {
//                directionsDisplay.setDirections(response);
//            }
//            });
//        }
}

