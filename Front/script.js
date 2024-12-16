document.addEventListener('DOMContentLoaded', function() {


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
        iconUrl: 'img/gaming.png',
        iconSize: [38, 95], 
        iconAnchor: [19, 47], // marker's location
        popupAnchor: [-3, -76] // popup should open relative to the iconAnchor
    });

    // Add marker with the icon
    // L.marker([48.8566, 2.3522], { icon: iconIp1 }).addTo(map)
    //     .bindPopup("I am IP1 icon!")
    //     .openPopup();

    /////////////////// ICON IP 2 /////////////////////////

    var iconIp2 = L.icon({
        iconUrl: 'img/ip2img.png',
        iconSize: [38, 95], 
        iconAnchor: [20, 48], // marker's location
        popupAnchor: [-3, -76] // popup should open relative to the iconAnchor
    });


    // Go Axios psk j'aime pas fetch
    async function fetchLastMessageAxiosIP1() {
        const response = await axios.get('http://localhost:8000/messages/IP1/last');
        console.log(response);
        console.log(response.data);
        return response.data;
    }

    async function fetchLastMessageAxiosIP2() {
        const response = await axios.get('http://localhost:8000/messages/IP2/last');
        console.log(response);
        console.log(response.data);
        return response.data;
    }

    // Pour debug les msg
    async function printLastMessage() {
        const lastMessage = await fetchLastMessageAxios();
        if (lastMessage) {
            console.log("Message trouvé:", lastMessage);
            const messageDiv = document.getElementById('message');
            messageDiv.innerHTML = `ID: ${lastMessage.id}, IP: ${lastMessage.IP}, Latitude: ${lastMessage.latitude}, Longitude: ${lastMessage.longitude}, Date: ${lastMessage.messageDate}`;
        } else {
            console.log("Aucun message disponible.");
        }
    }

    var markerIP1;
    // ajouter de la gestion d'erreur
    async function displayLastMessageIP1(){
        const lastMessage = await fetchLastMessageAxiosIP1();
        if (lastMessage) {
            markerIP1 = L.marker([lastMessage.latitude, lastMessage.longitude], { icon: iconIp1 }).addTo(map)
                .bindPopup(`IP: ${lastMessage.IP}, Latitude: ${lastMessage.latitude}, Longitude: ${lastMessage.longitude}, Date: ${lastMessage.messageDate}`)
                .openPopup();
        } else {
            console.log("IP1 Aucun message.");
        }
    }


    var markerIP2;
    // ajouter de la gestion d'erreur
    async function displayLastMessageIP2(){
        const lastMessage = await fetchLastMessageAxiosIP2();
        if (lastMessage) {
            markerIP2 = new L.marker([lastMessage.latitude, lastMessage.longitude], { icon: iconIp2 }).addTo(map)
                .bindPopup(`IP: ${lastMessage.IP}, Latitude: ${lastMessage.latitude}, Longitude: ${lastMessage.longitude}, Date: ${lastMessage.messageDate}`)
                .openPopup();
        } else {
            console.log("IP2 Aucun message.");
        }
    }

    printLastMessage();
    displayLastMessageIP1();
    displayLastMessageIP2();

    // setInterval(printLastMessage, 1000)
    setInterval(displayLastMessageIP1, 5000);
    setInterval(displayLastMessageIP2, 5000);
});