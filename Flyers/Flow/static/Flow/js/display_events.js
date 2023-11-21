const section_events = document.querySelector(".events_flow");

//let actuals = JSON.parse('{{ list_events }}')
//let list_events = document.getElementById("list_events")

/*const test = document.createElement("div")
test.innerText = list_events
section_events.appendChild(test)*/

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function printEvent(ev) {
    const elem = document.createElement("article")
    const elemTitle = document.createElement("h3")
    const elemDesc = document.createElement("p")
    const elemDateEv = document.createElement("p")
    const elemCreator = document.createElement("h4")
    const elemDateCreation = document.createElement("p")
    const elemImg = document.createElement("img")
    const elemRoadmap = document.createElement("div")
    const elemLikes = document.createElement("button")

    elemTitle.innerText = ev["title"]
    elemDesc.innerText = "description : "+ev["description"]
    elemDateEv.innerText = "date : "+ev["date"]
    elemCreator.innerText = "organisateur : "+ev["created_by"]
    const jour = ev["created_at"][8]+ev["created_at"][9]
    const mois = ev["created_at"][5]+ev["created_at"][6]
    const annee = ev["created_at"][0]+ev["created_at"][1]+ev["created_at"][2]+ev["created_at"][3]
    elemDateCreation.innerText = "date de création : "+jour+"/"+mois+"/"+annee+" à "+ev["created_at"][11]+ev["created_at"][12]+"h"+ev["created_at"][14]+ev["created_at"][15]
    elemImg.src = ev["image"]

    elemLikes.class = "btn-likes"
    elemLikes.addEventListener("click", function() {
        const elementId = ev.pk;  // Remplacez par l'ID de l'élément que vous souhaitez mettre à jour

        fetch('/update-like/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')  // Assurez-vous d'ajuster la récupération du jeton CSRF
            },
            body: new URLSearchParams({
                'element_id': elementId
            })
            })
            .then(response => response.json())
            .then(data => {console.log(data)
                if (data.success) {
                    console.log('Mise à jour réussie! Nouveau nombre de likes :', data.new_likes);
                } else {
                    console.error('Erreur lors de la mise à jour.');
                }
            })
            .catch(error => console.error('Erreur lors de la requête fetch :', error));
    });
    elemLikes.innerText = "Likes : " + ev["Likes"]

    elem.appendChild(elemTitle)
    elem.appendChild(elemDesc)
    elem.appendChild(elemDateEv)
    elem.appendChild(elemCreator)
    elem.appendChild(elemDateCreation)
    elem.appendChild(elemImg)
    elem.appendChild(elemRoadmap)
    elem.appendChild(elemLikes)

    return elem
}

for (let i = 0; i < list_events.length; i++) {
    const ev = list_events[i]["fields"]; // on récupère le prochain événement de la DB
    section_events.appendChild(printEvent(ev))
    const espace = document.createElement("br")
    section_events.appendChild(espace)
}