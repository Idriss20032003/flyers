const section_events = document.querySelector(".events_flow");

//let actuals = JSON.parse('{{ list_events }}')
//let list_events = document.getElementById("list_events")

/*const test = document.createElement("div")
test.innerText = list_events
section_events.appendChild(test)*/

function printEvent(ev) {
    const elem = document.createElement("article")
    const elemTitle = document.createElement("h3")
    const elemDesc = document.createElement("p")
    const elemDateEv = document.createElement("p")
    const elemCreator = document.createElement("h4")
    const elemDateCreation = document.createElement("p")
    const elemImg = document.createElement("img")
    const elemRoadmap = document.createElement("div")
    const elemLikes = document.createElement("p")

    elemTitle.innerText = ev["title"]
    elemDesc.innerText = "description : "+ev["description"]
    elemDateEv.innerText = "date : "+ev["date"]
    elemCreator.innerText = "organisateur : "+ev["created_by"]
    elemDateCreation.innerText = "date de création : "+ev["created_at"]
    elemImg.src = ev["image"]

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