$(document).ready(function() {
    $('#loginForm').validate({
        rules: {
            email: {
                required: true,
                email: true
            },
            password: {
                required: true,
                minlength: 8
            }
        },
        messages: {
            email: "Please enter a valid email address.",
            password: {
                required: "Please enter a password.",
                minlength: "Your password must be at least 8 characters long."
            }
        },
        submitHandler: function(form) {
            form.submit();
        }
    })
});