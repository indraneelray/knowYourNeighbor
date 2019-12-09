$(document).ready(function() {
    document.getElementById('logoutBtn').style.visibility='hidden';
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#imagePreview').css('background-image', 'url('+e.target.result +')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function() {
        readURL(this);
    });
    $('#signUpForm').validate(
        {
            rules: {
                fname: "required",
                lname: "required",
                email: {
                    required: true,
                    email: true
                },
                password: {
                    required: true,
                    minlength: 8
                },
                confirm_password: {
                    required: true,
                    minlength: 8,
                    equalTo: "#password"
                },
                gender: "required",
                addressLine1: "required",
                addressLine2: "required",
                city: "required",
                state: "required",
                zipcode: "required",
                email_pref: "required"
            },
            messages : {
                fname: "Please enter first name.",
                lname: "Please enter last name.",
                email: "Please enter a valid email address.",
                password: {
                    required: "Please enter a password.",
                    minlength: "Your password must be at least 8 characters long."
                },
                confirm_password: {
                    equalTo: "Passwords dont match."
                }
            }
        }
    )
})