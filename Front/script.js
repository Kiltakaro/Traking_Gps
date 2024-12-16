document.addEventListener('DOMContentLoaded', function() {


    // Initialisation de la carte sur une position (latitude, longitude) et un niveau de zoom
    var map = L.map('map').setView([48.8566, 2.3522], 13); // Paris

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    

    // https://leafletjs.com/examples/custom-icons/
    // En gros faire icon puis faire le point sur la map
    var marioIcon = L.icon({
        iconUrl: 'img/gaming.png',
        iconSize: [38, 95], 
        iconAnchor: [19, 47], // marker's location
        popupAnchor: [-3, -76] // popup should open relative to the iconAnchor
    });

    // Add marker with the icon
    L.marker([48.8566, 2.3522], { icon: marioIcon }).addTo(map)
        .bindPopup("I am a custom icon!")
        .openPopup();



    // Axios psk Fetch me deteste
    async function fetchLastMessageAxios() {
        const response = await axios.get('http://localhost:8000/messages/last');
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

    // Dupliquer pour IP2 et forcé celui ci sur IP1
    async function displayLastMessage(){
        const lastMessage = await fetchLastMessageAxios();
        if (lastMessage) {
            L.marker([lastMessage.latitude, lastMessage.longitude], { icon: marioIcon }).addTo(map)
            .bindPopup(`IP: ${lastMessage.IP}, Latitude: ${lastMessage.latitude}, Longitude: ${lastMessage.longitude}, Date: ${lastMessage.messageDate}`)
            .openPopup();
        } else {
            console.log("Aucun message disponible.");
        }
    }

    printLastMessage();
    displayLastMessage();
});