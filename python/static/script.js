$(document).ready(function () {

    // Initiera Select2
    $('#from').select2({
        placeholder: "Välj hållplats"
    });

    $('#to').select2({
        placeholder: "Välj hållplats"
    });

    // Ladda hållplatser från JSON
    fetch("/static/stops_skane.json")
        .then(response => response.json())
        .then(stops => {
            stops.forEach(stop => {
                const optionFrom = new Option(stop.name, stop.id, false, false);
                const optionTo = new Option(stop.name, stop.id, false, false);

                $('#from').append(optionFrom);
                $('#to').append(optionTo);
            });

            // Uppdatera Select2 efter att options lagts till
            $('#from').trigger('change');
            $('#to').trigger('change');
        })
        .catch(error => {
            console.error("Kunde inte ladda hållplatser:", error);
        });

});
