// Function to make password visible/invisible
function TogglePassword() {
    var passwordFields = document.querySelectorAll('input[id="id_password"]');
    passwordFields.forEach(function(field) {
        if (field.type === "password") {
            field.type = "text";
        } else {
            field.type = "password";
        }
    });
}

// Changing type of chafilerd password for password type
document.addEventListener("DOMContentLoaded", function() {
    var passwordField = document.getElementById("id_password");
    if (passwordField) {
        passwordField.setAttribute("type", "password");
    }
});
