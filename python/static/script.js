$(document).ready(function () {
    $('#from').select2({
        placeholder: "Välj hållplats"
    });

    $('#to').select2({
        placeholder: "Välj hållplats"
    });

// HEAD
    const jsonPaths = [
        "/static/stops_skane.json",
        "./static/stops_skane.json",
        "../static/stops_skane.json",
        "static/stops_skane.json"
    ];

    function tryLoadStops(pathIndex) {
        if (pathIndex >= jsonPaths.length) {
            console.error("Kunde inte hitta stops_skane.json på någon sökväg");
            return;
        }

        fetch(jsonPaths[pathIndex])
            .then(response => {
                if (!response.ok) {
                    console.log(`Testar sökväg ${jsonPaths[pathIndex]} - misslyckades`);
                    tryLoadStops(pathIndex + 1);
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(stops => {
                console.log(`Hittade JSON-filen på: ${jsonPaths[pathIndex]}`, stops.length + " hållplatser laddade");

                stops.forEach(stop => {
                    //const optionFrom = new Option(stop.name, stop.id, false, false);
                   // const optionTo = new Option(stop.name, stop.id, false, false);
                   const optionFrom = new Option(stop.name, stop.name, false, false);
                   const optionTo   = new Option(stop.name, stop.name, false, false);



                    $('#from').append(optionFrom);
                    $('#to').append(optionTo);
                });

                // Uppdatera Select2 efter att options lagts till
                $('#from').trigger('change');
                $('#to').trigger('change');
            })
            .catch(error => {
                if (error.message !== 'Network response was not ok') {
                    console.error("Kunde inte ladda hållplatser:", error);
                }
            });
    }

    // Börja med första sökvägen
    tryLoadStops(0);
});

function getCookie() {
    document.getElementById("login").innerHTML = document.cookie;
    return document.cookie;
}