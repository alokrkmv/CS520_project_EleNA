var routeInMarkers = []

$(document).ready(function(){
    $('#submitform').click(function(e) {
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
            for (let item of response.route) {
              temp = {}
              temp['latitude'] = item[0].toString()
              temp['longitude'] = item[1].toString()
              routeInMarkers.push(temp)
            }
            console.log(routeInMarkers)
            initMap(routeInMarkers)
         })
        .catch(/**/);

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
      var mapOptions = {
        center: new google.maps.LatLng(markers[markers.length/2].latitude, markers[markers.length/2].longitude),
        zoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      };
      var map = new google.maps.Map(document.getElementById("map"), mapOptions);
      var positions = [];
      var icon;
      var marker;
      for (var i = 0; i < markers.length; i++) {
          positions.push(new google.maps.LatLng(markers[i].latitude, markers[i].longitude))
          if (i == 0 || i == markers.length - 1) {
                marker = new google.maps.Marker({
                    position: positions[i],
                    map: map,
                    title: 'Click me'
                });
            } else {
                marker = new google.maps.Marker({
                    position: positions[i],
                    map: map,
                    icon: {
                        path: google.maps.SymbolPath.CIRCLE,
                        scale: 0
                    },
                    title: 'Click me'
                });
            }
        }
        //Intialize the Path Array
        var path = new google.maps.MVCArray();
        //Intialize the Direction Service
        var service = new google.maps.DirectionsService();
        var flightPath = new google.maps.Polyline({
          path: positions,
          geodesic: true,
          strokeColor: '#4986E7'
        });
        flightPath.setMap(map);
}

