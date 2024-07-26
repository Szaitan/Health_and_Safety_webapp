// Set the countdown starting time in seconds
var countdownTime = 5;

// Update the count down every 1 second
var countdownFunction = setInterval(function() {

    // Display the countdown time
    var countdownElement = document.getElementById("countdown");
    if (countdownElement) {
        countdownElement.innerHTML = countdownTime + "s";
    }

    // Decrease the countdown time by 1
    countdownTime--;

    // If the countdown is over, write some text
    if (countdownTime < 0) {
        clearInterval(countdownFunction);
        window.location.href = "/projects_page";
    }
}, 1000);