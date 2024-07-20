// Two things must be done for it to work:
// 1) CSRF Token has to be added as metatagg in html: <meta name="csrf-token" content="{{ csrf_token }}">
// and in .js file const csrfToken = $('meta[name="csrf-token"]').attr('content');
// 2) We have to pass url by adding in html: data-url="{% url 'remove_user_from_project' %}" and
// in .js create of variable const url = $(this).data('url') in anchor tah;

$(document).ready(function() {
    $('.remove-user').on('click', function(event) {
        event.preventDefault();
        if (confirm("Are you sure you want to remove this user from this project?")) {
            const userId = $(this).data('user-id');
            const projectName = $(this).data('project-name');
            const userFullName = $(this).data('user-fullname');
            const csrfToken = $('meta[name="csrf-token"]').attr('content');
            const url = $(this).data('url');

            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'user_id': userId,
                    'project_name': projectName,
                    'csrfmiddlewaretoken': csrfToken
                },
                success: function(response) {
                    if (response.success) {
                        $('#user-' + userId).remove();
                        alert(`User: ${userFullName} has been removed.`);
                    }
                },
                error: function(response) {
                    alert('An error occurred while trying to remove the user.');
                }
            });
        }
    });
});