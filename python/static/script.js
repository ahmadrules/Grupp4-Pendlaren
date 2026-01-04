function testSpotify() {
    const url =new URL(location.href)

    const obj = {
        "code" : url.searchParams.get("code")
    }
    console.log(obj)
    console.log("TESTING")
}

function getCookie() {
    document.getElementById("login").innerHTML = document.cookie;
    return document.cookie;
}

function renderStops(stops) {
    const list = document.querySelector(".playlist-aside .playlist-list");
    if (!list) return;

    list.innerHTML = "";

    if (!stops || stops.length === 0) {
        list.innerHTML = '<li class="playlist-item playlist-item--empty">Inga hållplatser hittades</li>';
        return;
    }

    for (const name of stops) {
        const li = document.createElement("li");
        li.className = "playlist-item";
        li.textContent = name;
        list.appendChild(li);
    }
}   

async function loadStopsFromQuery() {
    const url = new URL(window.location.href);
    const fromStop = url.searchParams.get("from");
    const toStop = url.searchParams.get("to");

    if (!fromStop || !toStop) return;

    const res = await fetch('/route_stops?from=${encodeURIComponent(fromStop)}&to=${encodeURIComponent(toStop)}');
    const data = await res.json();
    renderStops(data.stops);
}

document.addEventListener("DOMContentLoaded", loadStopsFromQuery);