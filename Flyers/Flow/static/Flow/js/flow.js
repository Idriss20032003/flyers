// ELEMENTS DU DOM HTML
//////////////////////////////////////////////////////////////////:



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

const fileSend = document.getElementById('fileSend')
const fileInput = document.getElementById('fileInput')
function sendFile () {
    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
        const fileData = e.target.result;
        const message = {'type': 'image', 'message': fileData};
        chatSocket.send(JSON.stringify(message));

    };
    reader.readAsDataURL(file);
}

if (fileSend) {
    fileSend.addEventListener('click', function (e){
e.preventDefault();
sendFile();
console.log('photo envoyée avec succès')
    })
}

// chatInputElement à utiliser dans le html des groupes
let chatInputElement = document.getElementById('chatInputElement')
function sendMessage(){
    chatSocket.send(JSON.stringify({
        'type': 'message',
        'message': chatInputElement.value,
    }));
    // chatSocket.send(JSON.stringify({
    //     'type': 'notification',
    //     'message': chatInputElement.value,
    // }));

};


let Chat_onwritting =document.getElementById('Chat_onwritting');

let chatLogElement = document.getElementById('chatLogElement');
function scrollToBottom() {
    chatLogElement.scrollTop = chatLogElement.scrollHeight
}

function displayImage(imageData) {
    const imageElement = document.createElement('img');
    imageElement.src = imageData;  
    chatLogElement.appendChild(imageElement);}

function onChatMessage(data, user_id = null) {
    console.log('onChatMessage', data)

    if (data.type == 'chat_message') {
        if (document.getElementById('is_tiping')) {
            document.getElementById('is_tiping').remove()
        }
        if (user_id == data.user_name) {
            chatLogElement.innerHTML += `<div class="message"> 
                                        <p class="content_message">${data.message}</p> 
                                        <i><p class ="message_infos">${data.created_at}-${data.user_name}</p></i>
                                        </div>` //ajouter le style adéquat!
        }
        else {
            chatLogElement.innerHTML += `<div class="message"> 
            <p class="content_message">${data.message}</p> 
            <i><p class ="message_infos">${data.created_at}-${data.user_name}</p></i>
            </div>` //ajouter le style adéquat!
        }
    }
    else if (data.type == 'writting_active') {
        if(! user_id==data.user_name){
            Chat_onwritting.innerHTML=
        `<div class="is_tiping"><i>${data.user_name} is typing</i></div>` //ajouter le style adéquat!
        }
    }
    else if (data.type == 'chat_image') {
        // Supposons que vous ayez déjà une connexion WebSocket nommée 'socket'
        displayImage(data.message);
        console.log('photo reçue')

// Fonction pour afficher les messages dans la boîte de chat


// Fonction pour afficher les images dans la boîte de chat

};

// Gestionnaire d'événements pour les messages WebSocket

    // if (data.type == 'chat_notification') {
    //     if (user_id !== data.sender_id){
    //         alert(`${data.user_name} a envoyé un message dans '${data.room}'`)
    //     }
    // };
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
    });}
    if (chatInputElement) {
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

if (chatInputElement) {
    chatInputElement.onfocus = function(e) {
        chatSocket.send(JSON.stringify({
            'type': 'update',
            'message': 'writing_active',
        }))
    }
    
}

// CREATTION DE L'EVENT ET DE LA CHATROOM ASSOCIEE 
////////////////////////////////////////////////////////////////////////////////

// chatlOG correspondra en html à la zone d'affichage des messages 
// Si c'est l'utilisateur connecté qui envoie le message, alors il s'affiche à gauche, sinon à droite
let EventCreated = document.getElementById('Cevent')    
console.log(EventCreated);
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
            alert(`L'évènement a été créé, retrouvez ses membres dans vos communautés !`)

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
    window.location.href = '/'; // Redirection vers la page d'accueil

            };


            chatSocket.onclose = function(e) {
                console.log('onClose - chat socket was closed');
            };

           
        }
    })
});

