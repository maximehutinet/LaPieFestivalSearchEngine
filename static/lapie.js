$('.card').hide();
let mymap = L.map('map');
let markers = L.markerClusterGroup();
let eventIds = [];
let latitude  = 46.823;
let longitude = 7.539;
let radius = 7;
NProgress.configure({ easing: 'ease', speed: 700 });

// Hide the card if the user clicks on the navbar
$('.navbar').on('click', function (e) {
    $('.card').hide();
});

// Hide the card collapse if the user clicks on the map
$('#map').click(function(e) {
	if (!$(e.target).is('.form-group')) {
    	$('.collapse').collapse('hide');
    }
});

// Hide the card
$('#map').on('click', function(e) {
    e.stopPropagation();
});

// Submit the name of the person to the server
$('#interestedForm').submit(function (event) {
    let name = $('#inputName').val() + ', ' + $('#interestedText').text();
    let currentEventId = $('#eventfulID').text();
    socket.emit('my event', {eventfulID : currentEventId, interestedPersonName: name});
    $('.collapse').collapse('hide');
    let form = document.getElementById("interestedForm");
    form.reset();
    event.preventDefault();
});

// Display the name of the person who's interested
function onReceiveInterested(data){
        $('#interested').show('slow');
        if($('.card').is(':contains(' + data['eventfulID'] + ')')){
            let interestedPersons = data['interestedPersonName'];
            $('#interestedText').html(interestedPersons);
    }
}

// Websocket
let socket = io.connect({
  'path': window.location.pathname + 'socket.io'
});
socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
});
socket.on('my response', function(msg) {
    onReceiveInterested(msg);
});

// Get map radius to target events in a specific scope
function getMapRadiusKM(){
    let mapBoundNorthEast = mymap.getBounds().getNorthEast();
    let mapDistance = mapBoundNorthEast.distanceTo(mymap.getCenter());
    return mapDistance/1000;
}

// Get artist information
function getArtistInformation(artistId, artistInformation) {
    if (artistId != null) {
        let uri = 'artist/' + artistId;
        NProgress.start();
        $.getJSON(uri, function (data) {
            artistInformation(data);
            NProgress.inc(0.2);
            NProgress.done();
        });
    }else{
        artistInformation(null);
    }
}

// Function triggered when a marker (event) is selected on the map
function onEventClick(data) {
    $('.card-header').html('<img src="static/ajax-loader.gif" alt="Loading"> Loading...');
    $('#interestedText').html('');
    getArtistInformation(data['artist'][0], function(artistInformation){
        // Get top track of one of the artists
        try {
            let toptrack = Object.values(artistInformation['artistTopTrack'])[0];
            toptrackbeacon = '<br><audio controls autoplay><source src="' + toptrack.toString() + '" type="audio/ogg">Your browser does not support the audio element.</audio>';
        }catch(err) {
            toptrackbeacon = '';
        }

        try {
            let coverimage = artistInformation['pictureLinks'][0];
            eventimagebeacon = '<img src="'+coverimage+'" alt="Event Image" width="320px">';
        }catch(err) {
            eventimagebeacon = '';
        }

        mymap.setView([data['latitude'], data['longitude']]);
        $('.card-header').html(data['event-name']);
        $('.card-title').html(data['venue-name']);
        $('.card-text').html(
            eventimagebeacon+
            toptrackbeacon+
            '<br><b>Location:</b> '+data['address'] +' - ' + data['city-name']+' - '+data['country-name']+
            '<br><b>Start Time:</b> '+data['event-start-time']
        );
        $('#eventfulID').html(data['eventfulID']);

        if (!$('.collapseDetailsButton').is(':visible')){
            $('.more-details').html(
            '<br><b>Description:</b> '+data['description']
        );
        }


        try {
            if(data['interestedPersonName']){
                $('#interested').show('slow');
                $('#interestedText').html(data['interestedPersonName']);
            }else{
                $('#interested').hide('slow');
            }
        }
        catch (e) {
            console.log("No one interested");
        }
        $('.card').show();
    });

}

// Get events based on a radius and place them on the map
function getEvents(){
    //markers.clearLayers();
    latitude = mymap.getCenter()['lat'];
    longitude = mymap.getCenter()['lng'];
    radius = getMapRadiusKM();
    let uri = 'events?latitude='+latitude+'&longitude='+longitude+'&radius='+radius;
    NProgress.start();
    $.getJSON(uri, function(data){
        for (let event in data.events) {
            try{
                if(data.events[event]['latitude'] != null && data.events[event]['longitude'] != null) {
                if(!eventIds.includes(data.events[event]['eventfulID'])) {
                    markers.addLayer(L.marker([data.events[event]['latitude'], data.events[event]['longitude']]).on('click', function (e) {
                        $('.card-header').html('<img src="static/ajax-loader.gif" alt="Loading"> Loading...');
                        onEventClick(data.events[event]);
                    }));
                    eventIds.push(data.events[event]['eventfulID'])

                }
            }
            NProgress.inc(0.2);
            }
            catch (TypeError) {
                console.log("There is an even with wrong data type")
            }
        }
        NProgress.done();
    });
    mymap.addLayer(markers);
}

// Get city coordinates from openstreetmap
function getCity(name) {
    let uri = 'https://nominatim.openstreetmap.org/search?city='+name+'&format=json';
    $.getJSON(uri, function(data){
        mymap.setView([data[0]['lat'], data[0]['lon']]);
        getEvents();
    });
}

// Function called when the browser geolocation worked
function geoLocationSuccess(position) {
    latitude  = position.coords.latitude;
    longitude = position.coords.longitude;
    radius = 13;
    mymap.setView([latitude, longitude], radius);
}

// Function called when the browser geolocation failed
function geoLocationError() {
    console.log('The location coudln\'t be retrieved from the browser.');
    mymap.setView([latitude, longitude], radius);
}

// Get geolocation from browser
navigator.geolocation.getCurrentPosition(geoLocationSuccess, geoLocationError);

let img = new Image();
img.src = "https://maps.googleapis.com/maps/api/staticmap?center=" + latitude + "," + longitude + "&zoom=13&size=300x300&sensor=false";

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox.streets'
}).addTo(mymap);

// Reload events when the map is dragged
mymap.on('dragend',function(e){
    getEvents();
});

// Reload events when the user zooms into the map
mymap.on('zoom',function(e){
    getEvents();
});

// Search for a city, get coordinates and reload the map
$('#search-city').submit(function () {
    getCity($('#search-city input').val());
    return false;
});
