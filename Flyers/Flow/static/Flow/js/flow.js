
 async function JoinGroupRoom (event) {

    event.preventDefault(); 
        // Récupérer les valeurs des champs du formulaire
        var formData = new FormData(this); // Obtenir les données du formulaire
        const event_id = formData
    
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

        chatSocket = new WebSocket(`ws://${window.location.host}/ws/${event_id}/`)

        chatSocket.onmessage = function(e) {
            console.log('onMessage')
        }

        chatSocket.onopen = function(e) {
            console.log('onOpen - chat socket was opened')
        }

        chatSocket.onclose = function(e) {
            console.log('onClose - chat socket was closed')
        }
    }

let EventCreated = document.getElementById('NouvelEvent')
let e = EventCreated.value
EventCreated.addEventListener('submit', JoinGroupRoom(e))