// ELEMENTS DU DOM HTML
//////////////////////////////////////////////////////////////////:

let EventCreated = document.getElementById('Cevent')    
console.log(EventCreated);

let eId = null; 


// WEBSOCKET GESTIONNAIRE COTE CLIENT
//////////////////////////////////////////////////////////////////////////////////

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
    };
    return cookieValue;
};


// chatInputElement à utiliser dans le html des groupes
let chatInputElement = document.getElementById('chatInputElement')
function sendMessage(){
    chatSocket.send(JSON.stringify({
        'type': 'message',
        'message': chatInputElement.value,
    }));
};
let chatLogElement = document.getElementById('chatLogElement')
function scrollToBottom() {
    chatLogElement.scrollTop = chatLogElement.scrollHeight
}
function onChatMessage(data, user_id = null) {
    console.log('onChatMessage', data)

    if (data.type == 'chat_message') {
        if (user_id == data.sender_id) {
            chatLogElement.innerHTML += `<div class="message"> 
                                        <p class="content_message">${data.message}</p> 
                                        <i><p class ="message_infos">${data.created_at}-${data.initials}</p></i>
                                        </div>` //ajouter le style adéquat!
        }
        else {
            chatLogElement.innerHTML += `<div class="message"> 
            <p class="content_message">${data.message}</p> 
            <i><p class ="message_infos">${data.created_at}-${data.initials}</p></i>
            </div>` //ajouter le style adéquat!
        }
    };
    setTimeout(scrollToBottom(), 100); // Essaie d'ajouter un léger délai avant le défilement
}

// ENVOI DE MESSAGE PAR L UTILISATEUR EN FRONTEND 
chatSubmitElement=document.getElementById('EnvoiMess')
if (chatSubmitElement) {
    chatSubmitElement.addEventListener('click', function(e) {
        e.preventDefault();
        const message = chatInputElement.value.trim(); // Récupère le contenu du champ et enlève les espaces au début et à la fin
        
        if (message !== '') {
            sendMessage();
            chatInputElement.value = '';
        } else {
        }
    });

    chatInputElement.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            const message = chatInputElement.value.trim(); // Récupère le contenu du champ et enlève les espaces au début et à la fin
            
            if (message !== '') {
                sendMessage();
                chatInputElement.value = '';
            } else {
            }
        }
    });
}


// CREATTION DE L'EVENT ET DE LA CHATROOM ASSOCIEE 
////////////////////////////////////////////////////////////////////////////////

// chatlOG correspondra en html à la zone d'affichage des messages 
// Si c'est l'utilisateur connecté qui envoie le message, alors il s'affiche à gauche, sinon à droite

EventCreated.addEventListener('submit', function (event) {    

    event.preventDefault(); 
    // Récupérer les valeurs des champs du formulaire
    const formData = new FormData(EventCreated); // Obtenir les données du formulaire    
    console.log(formData);
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
                setTimeout(scrollToBottom(), 100); // Essaie d'ajouter un léger délai avant le défilement

            };

            chatSocket.onclose = function(e) {
                console.log('onClose - chat socket was closed');
            };
        }
    });
});









