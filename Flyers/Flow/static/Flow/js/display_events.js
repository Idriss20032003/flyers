//const section_events = document.querySelectorAll(".event-card");

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

function printEvent(ev_model) {
    const ev = ev_model["fields"]
    const elemLikes = document.getElementById(ev_model["pk"])
    //divLikes.attr="{{ev_model.pk}}"
    /*const elem = document.createElement("article")
    const elemTitle = document.createElement("h3")
    const elemDesc = document.createElement("p")
    const elemDateEv = document.createElement("p")
    const elemCreator = document.createElement("h4")
    const elemDateCreation = document.createElement("p")
    const elemImg = document.createElement("img")
    const elemRoadmap = document.createElement("div")*/
    //const elemLikes = document.createElement("button")
    //elemLikes.attr="{{ev_model.pk}}"

    /*elemTitle.innerText = ev["title"]
    elemDesc.innerText = "description : "+ev["description"]
    elemDateEv.innerText = ev["date"]
    elemCreator.innerText = "organisateur : "+ev["created_by"]
    const jour = ev["created_at"][8]+ev["created_at"][9]
    const mois = ev["created_at"][5]+ev["created_at"][6]
    const annee = ev["created_at"][0]+ev["created_at"][1]+ev["created_at"][2]+ev["created_at"][3]
    elemDateCreation.innerText = "date de création : "+jour+"/"+mois+"/"+annee+" à "+ev["created_at"][11]+ev["created_at"][12]+"h"+ev["created_at"][14]+ev["created_at"][15]
    let divImg = document.createElement("div")
    divImg.className = "divImg"
    let img = ev["image"]
    elemImg.src = `./media/${img}`*/

    //let divLikes = document.createElement("div")
    //divLikes.className = "event-card-likes"
    //elemLikes.class = "btn-likes"
    elemLikes.addEventListener("click", function(e) {
        const elementId = ev_model["pk"]; // id de l'élément qu'on souhaite mettre à jour
        console.log(elementId)
        e.preventDefault()
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
                location.reload()
            })
            .catch(error => console.error('Erreur lors de la requête fetch :', error));
    });
    elemLikes.innerText = "Likes : " + ev["Likes"].toString()

    /*elem.appendChild(elemDateEv)
    elem.appendChild(elemTitle)
    elem.appendChild(elemDesc)
    elem.appendChild(elemCreator)
    elem.appendChild(elemDateCreation)
    divImg.appendChild(elemImg)
    console.log(divImg)
    elem.appendChild(divImg)
    elem.appendChild(elemRoadmap)*/
    //divLikes.appendChild(elemLikes)
    //elem.appendChild(divLikes)

   //return elem
}

for (let i = 0; i < serialized_events.length; i++) {
    const ev_model = serialized_events[i] // on récupère le prochain événement de la DB
    printEvent(ev_model)
    /*const espace = document.createElement("br")
    section_events.appendChild(espace)*/
}