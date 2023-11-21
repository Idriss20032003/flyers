// ELEMENTS DU DOM HTML
//////////////////////////////////////////////////////////////////:
// let chatLogElement = document.getElementById('ChampMessages')

// // chatInputElement à utiliser dans le html des groupes
// let chatInputElement = document.getElementById('Zone chat')

let EventCreated = document.getElementById('NouvelEvent')

// FONCTION CONNEXION AU SOCKET 
function ConnectSocket(u) {
    chatSocket = new WebSocket(`ws://${window.location.host}/ws/${u}/`)

            chatSocket.onmessage = function(e) {
                console.log('onMessage');
                const data = JSON.parse(e.data);
                const user_id = data.user_id;
                console.log('User ID received from server:', user_id);
                onChatMessage(data, user_id);
            };

            chatSocket.onopen = function(e) {
                console.log('onOpen - chat socket was opened');
            };

            chatSocket.onclose = function(e) {
                console.log('onClose - chat socket was closed');
            };
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Recherche du jeton CSRF dans les cookies
            if (cookie.startsWith(`${name}=`)) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// CREATTION DE L'EVENT ET DE LA CHATROOM ASSOCIEE 
////////////////////////////////////////////////////////////////////////////////

// chatlOG correspondra en html à la zone d'affichage des messages 
// Si c'est l'utilisateur connecté qui envoie le message, alors il s'affiche à gauche, sinon à droite
let eId = 0 

EventCreated.addEventListener('submit', function (event) {    
    
    event.preventDefault(); 
    
    // Récupérer les valeurs des champs du formulaire
    const formData = new FormData(EventCreated); // Obtenir les données du formulaire    
    console.log(formData);
    // function put (i) {eId = i} 

    fetch('/create_event/', {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    }).then(data => {
        if (data.success) {
            eId = data.event_id;
            console.log('L\'événement a été créé avec succès. ID :', eId);

            return fetch(`/api/create-room/${eId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
        } else {
            console.error('Erreur lors de la création de l\'événement:', data.error);
        }
    }).then(res => {
        if (res) {
            return res.json();
        }
    }).then(data => {
        if (data) {
            console.log('data', data);
            // Le reste de ton code pour la création du socket, etc.

            chatSocket = new WebSocket(`ws://${window.location.host}/ws/${eId}/`)

            chatSocket.onmessage = function(e) {
                console.log('onMessage');
                const data = JSON.parse(e.data);
                const user_id = data.user_id;
                console.log('User ID received from server:', user_id);
                onChatMessage(data, user_id);
            };

            chatSocket.onopen = function(e) {
                console.log('onOpen - chat socket was opened');
            };

            chatSocket.onclose = function(e) {
                console.log('onClose - chat socket was closed');
            };
        }
    });


    // Création du socket associé et connexion du créateur de l'event au websocket 

    

});




// WEBSOCKET GESTIONNAIRE COTE CLIENT
//////////////////////////////////////////////////////////////////////////////////



