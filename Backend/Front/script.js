document.addEventListener('DOMContentLoaded', function () {


    // Initialisation de la carte sur une position (latitude, longitude) et un niveau de zoom
    var map = L.map('map').setView([48.8566, 2.3522], 13); // Paris

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);


    /////////////////// ICON IP 1 /////////////////////////


    // https://leafletjs.com/examples/custom-icons/
    // En gros faire icon puis faire le point sur la map
    var iconIp1 = L.icon({
        iconUrl: 'static/img/ip1img.png',
        iconSize: [38, 95],
        iconAnchor: [19, 47], // marker's location
        popupAnchor: [-3, -76] // popup should open relative to the iconAnchor
    });


    /////////////////// ICON IP 2 /////////////////////////

    var iconIp2 = L.icon({
        iconUrl: 'static/img/ip2img.png',
        iconSize: [38, 95],
        iconAnchor: [20, 48], // marker's location
        popupAnchor: [-3, -76] // popup should open relative to the iconAnchor
    });


    //////////////////// TENTATIVE WEBSOCKET //////////////////////


    var markerIP1;
    var markerIP2;

    // Connexion WebSocket

    const socket = new WebSocket(`ws://localhost:8000/ws`);

    socket.onopen = function(event) {
        console.log("WebSocket is open now.");
    };
    socket.onmessage = function(event) {
        const lastMessageNewFormat = JSON.parse(event.data);
        console.log("Message reçu via WebSocket:", lastMessageNewFormat);

        if (lastMessageNewFormat) {
            if (markerIP1) {
                markerIP1.remove();
            }
            // on pourra mondifier le popup mais la ça sert a debug
            markerIP1 = L.marker([lastMessageNewFormat.latitudeIP1, lastMessageNewFormat.longitudeIP1], { icon: iconIp1 }).addTo(map)
                .bindPopup(`IP: ${lastMessageNewFormat.IP1}, Latitude: ${lastMessageNewFormat.latitudeIP1}, Longitude: ${lastMessageNewFormat.longitudeIP1}, Date: ${lastMessageNewFormat.messageDateIP1}`)
                .openPopup();

            if (markerIP2) {
                markerIP2.remove();
            }
            markerIP2 = L.marker([lastMessageNewFormat.latitudeIP2, lastMessageNewFormat.longitudeIP2], { icon: iconIp2 }).addTo(map)
                .bindPopup(`IP: ${lastMessageNewFormat.IP2}, Latitude: ${lastMessageNewFormat.latitudeIP2}, Longitude: ${lastMessageNewFormat.longitudeIP2}, Date: ${lastMessageNewFormat.messageDateIP2}`)
                .openPopup();
        }
    };
    socket.onclose = function(event) {
        console.log("WebSocket fermé:", event);
    };
    socket.onerror = function(error) {
        console.error("WebSocket erreur:", error);
    };

});
