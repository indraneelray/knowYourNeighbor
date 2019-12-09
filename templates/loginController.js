
    $().ready(function() {
	document.getElementById('logoutBtn').style.visibility='hidden';
        $('#loginForm').validate({
            rules: {
                email: {
                    required: true,
                    email: true
                },
                pwd: {
                    required: true,
                    minlength: 8
                }
            },
            messages: {
                email: "Please enter a valid email address.",
                pwd: {
                    required: "Please enter a password.",
                    minlength: "Your password must be at least 8 characters long."
                }
            },
            submitHandler: function(form) {
                form.submit();
            }
        })
    });

