
 async function JoinGroupRoom (event) {

        event.preventDefault(); 

        // Récupérer les valeurs des champs du formulaire
        var formData = new FormData(this); // Obtenir les données du formulaire    
        
        await fetch('create_event/', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // Gérer la réponse si la requête est réussie
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            // Traiter la réponse JSON en fonction du contenu
            if (data.success) {
                // Si la création de l'événement a réussi
                const event_id = data.eventID;
                console.log('L\'événement a été créé avec succès. ID :', event_id);
                // Autre action si nécessaire...
            } else {
                // Si la création de l'événement a échoué
                console.error('Erreur lors de la création de l\'événement:', data.error);
                // Autre action si nécessaire...
            }
        })
        .catch(error => {
            // Gérer les erreurs ici
            console.error('Error:', error);
        });
    
    
    
        await fetch(`api/create-room/${event_id}`, {
            method: 'POST',
            body: formData
        })
        .then( res => {
           return res.json
        })
        .then( data => { console.log('data',data)
    
        });


        // Création du socket associé 

        chatSocket = new WebSocket(`ws://${window.location.host}/ws/${event_id}/`)

        chatSocket.onmessage = function(e) {
            console.log('onMessage');
            const data = JSON.parse(e.data);
            const user_id = data.user_id;
            console.log('User ID received from server:', userId);
            onChatMessage(data, user_id);
        }

        chatSocket.onopen = function(e) {
            console.log('onOpen - chat socket was opened')
        }

        chatSocket.onclose = function(e) {
            console.log('onClose - chat socket was closed')
        }
    }
// chatlOG correspondra en html à la zone d'affichage des messages 
// Si c'est l'utilisateur connecté qui envoie le message, alors il s'affiche à gauche, sinon à droite

let chatLogElement = document.getElementById('ChampMessages')

// chatInputElement à utiliser dans le html des groupes
let chatInputElement = document.getElementById('Zone chat')

function sendMessage(){
    chatSocket.sendMessage(JSON.stringify({
        'type': 'message',
        'message': chatInputElement.value,
        'name': chatName
    }))

    chatInputElement.value == ''
}

function onChatMessage(data, user_id = None) {
    console.log('onChatMessage', data)

    if (data.type == 'chat_message') {
        if (user_id == data.sender_id) {
            chatLogElement.innerHTML += `<div class="message"> 
                                        <p class="content_message">${data.message}<\p> 
                                        <span class ="message_age">${data.created_at}<\span>
                                        <p class = "initials_message">${data.initials}<\p> 
                                        <\div>` //ajouter le style adéquat!
        }
        else {
            chatLogElement.innerHTML += `<div class="message"> 
                                        <p class = "initials_message">${data.initials}<\p> 
                                        <span class ="message_age">${data.created_at}<\span>
                                        <p class="content_message">${data.message}<\p> 
                                        <\div>` //ajouter le style adéquat!
        }
    }
}


let EventCreated = document.getElementById('NouvelEvent')
EventCreated.addEventListener('submit', function(event) {
    JoinGroupRoom(event)
    return False
})


// ChatSubmitElement à utiliser comme bouton pour envoyer un message dans le groupe
chatSubmitElement.addEventListener('click',function(e){
    e.preventDefault()
    sendMessage()
    return False
})

