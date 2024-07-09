document.addEventListener("DOMContentLoaded", function() {
    var iconGrid = document.getElementById('icon-grid');
    var iconGridOffset = iconGrid.offsetTop;
    var iconGridDisplayed = false;

    function handleScroll() {
        if (!iconGridDisplayed && window.pageYOffset + window.innerHeight > iconGridOffset) {
            iconGrid.classList.add('show');
            iconGridDisplayed = true;
            // Remove event listener to only animate once
            window.removeEventListener('scroll', handleScroll);
        }
    }

    window.addEventListener('scroll', handleScroll);
});
