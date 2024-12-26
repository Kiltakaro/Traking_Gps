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
    const ip_broker = "localhost" // IP du broker

    const socket = new WebSocket(`ws://${ip_broker}:8000/ws`);

    socket.onopen = function(event) {
        console.log("WebSocket is open now.");
    };
    socket.onmessage = function(event) {
        const lastMessageNewFormat = JSON.parse(event.data);
        console.log("Message reçu via WebSocket:", lastMessageNewFormat);

        if (lastMessageNewFormat) {

            ///////////////////// MARKER 1 //////////////////////////

            if (markerIP1) {
                markerIP1.remove(); // Supprime ancienne position pour mettre la nouvelle après 
            }
            if (lastMessageNewFormat.latitudeIP1 !== null) { 

                // Affiche sur la map la derniere position de IP1
                markerIP1 = L.marker([lastMessageNewFormat.latitudeIP1, lastMessageNewFormat.longitudeIP1], { icon: iconIp1 }).addTo(map)
                    .bindPopup(`IP: ${lastMessageNewFormat.IP1}, Latitude: ${lastMessageNewFormat.latitudeIP1}, Longitude: ${lastMessageNewFormat.longitudeIP1}, Date: ${lastMessageNewFormat.messageDateIP1}`)
                    .openPopup();
                
                // Affiche en dessous de la carte le dernier messageIP1
                // Transforme la date en pour la rendre plus lisible
                const dateObject1 = new Date(lastMessageNewFormat.messageDateIP1);
                const readableDateIP1 = dateObject1.toLocaleDateString("en-US", {
                    year: "numeric",
                    month: "long",
                    day: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                    second: "2-digit",
                });
                
                // Tronque les nombres à virgule
                const formattedLatitudeIP1 = formatCoordinate(lastMessageNewFormat.latitudeIP1, 5);
                const formattedLongitudeIP1 = formatCoordinate(lastMessageNewFormat.longitudeIP1, 5);

                const messageDiv1 = document.getElementById('messageIP1');
                messageDiv1.innerHTML = `
                    IP: ${lastMessageNewFormat.IP1},<br>
                    Latitude: ${formattedLatitudeIP1},<br>
                    Longitude: ${formattedLongitudeIP1},<br>
                    Date: ${readableDateIP1}
                `;            
            }
            ///////////////////// MARKER 2 //////////////////////////

            if (markerIP2) {
                markerIP2.remove(); // Supprime ancienne position pour mettre la nouvelle après 
            }
            // Affiche sur la map la derniere position de IP1
            if (lastMessageNewFormat.latitudeIP2 !== null) { 
                markerIP2 = L.marker([lastMessageNewFormat.latitudeIP2, lastMessageNewFormat.longitudeIP2], { icon: iconIp2 }).addTo(map)
                    .bindPopup(`IP: ${lastMessageNewFormat.IP2}, Latitude: ${lastMessageNewFormat.latitudeIP2}, Longitude: ${lastMessageNewFormat.longitudeIP2}, Date: ${lastMessageNewFormat.messageDateIP2}`)
                    .openPopup();
                
                // Affiche en dessous de la carte le dernier messageIP2
                // Transforme la date en pour la rendre plus lisible
                const dateObject2 = new Date(lastMessageNewFormat.messageDateIP2);

                const readableDateIP2 = dateObject2.toLocaleDateString("en-US", {
                    year: "numeric",
                    month: "long",
                    day: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                    second: "2-digit",
                });

                // Tronque les nombres à virgule
                const formattedLatitudeIP2 = formatCoordinate(lastMessageNewFormat.latitudeIP2, 5);
                const formattedLongitudeIP2 = formatCoordinate(lastMessageNewFormat.longitudeIP2, 5);
            
                const messageDiv2 = document.getElementById('messageIP2');
                messageDiv2.innerHTML = `
                    IP: ${lastMessageNewFormat.IP2},<br>
                    Latitude: ${formattedLatitudeIP2},<br>
                    Longitude: ${formattedLongitudeIP2},<br>
                    Date: ${readableDateIP2}
                `;              
            }
        }
    };
    socket.onclose = function(event) {
        console.log("WebSocket fermé:", event);
    };
    socket.onerror = function(error) {
        console.error("WebSocket erreur:", error);
    };

    // Fontion pour tronquer les virgules
    function formatCoordinate(coordinate, decimalPlaces = 5) {
        return coordinate.toFixed(decimalPlaces);
    }

});
