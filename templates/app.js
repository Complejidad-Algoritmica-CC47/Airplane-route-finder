function validateInputs() {
    var selectedMethod = document.getElementById("metodo").value;
    var sourceAirport = document.getElementsByName("sourceAirportId")[0].value;
    var destinationAirport = document.getElementsByName("destinationAirportId")[0].value;
    var submitButton = document.querySelector("button[type='submit']");

    if (sourceAirport && destinationAirport) {
        submitButton.removeAttribute("disabled");
    } else {
        submitButton.setAttribute("disabled", "disabled");
    }
}