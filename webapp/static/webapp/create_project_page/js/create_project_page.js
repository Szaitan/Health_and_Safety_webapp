function redirectAfterDelay(url, delay) {
    setTimeout(function() {
        window.location.href = url;
    }, delay);
}