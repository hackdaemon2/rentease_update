 // global javascript functions
 const validateEmail = (email, passwordsInfo) => {
     $(email).blur(function(event) {
         passwordsInfo.removeClass().html("");
     });

     $(email).keyup(function(event) {
         let regEx = /^(([A-Za-z]+)\.?(\w)*)+@(([\-\w]+)\.?)+\.[a-zA-Z]{2,4}$/;

         if (email.val() === "" || email.val() === null) {
             passwordsInfo.removeClass().html('');
         } else {
             if (regEx.test(email.val()) === false) {
                 passwordsInfo.removeClass().addClass('weakpass').html("Enter a valid email address");
             } else {
                 passwordsInfo.removeClass().html("");
             }
         }
     });
 };

 const validateEmailAddress = (email) => {
     let regEx = /^(([A-Za-z]+)\.?(\w)*)+@(([\-\w]+)\.?)+\.[a-zA-Z]{2,4}$/;

     if (regEx.test(email) === false) {
         return false;
     } else {
         return true;
     }
 };

 const passwordEqualityCheck = (password1, password2, passwordsInfo) => {
     $(password2).blur(function(event) {
         passwordsInfo.removeClass().html("");
     });

     $(password2).keyup(function(event) {
         if (password1.val() !== password2.val()) {
             passwordsInfo.removeClass().addClass('weakpass').html("Confirm Password must match Password");
         } else {
             passwordsInfo.removeClass().html("");
         }
     });
 };

 const passwordStrengthCheck = (password1, passwordsInfo) => {
     //Must contain 6 characters or more
     var WeakPass = /(?=.{6,}).*/;
     //Must contain lower case letters and at least one digit.
     var MediumPass = /^(?=\S*?[a-z])(?=\S*?[0-9])\S{6,}$/;
     //Must contain at least one upper case letter, one lower case letter and one digit.
     var StrongPass = /^(?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9])\S{6,}$/;
     //Must contain at least one upper case letter, one lower case letter and one digit.
     var VryStrongPass = /^(?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9])(?=\S*?[^\w\*])\S{6,}$/;

     $(password1).keyup(function(event) {
         if (password1.val() === "") {
             passwordsInfo.removeClass().html("");
         } else {

             if (VryStrongPass.test(password1.val())) {
                 passwordsInfo.removeClass().addClass('vrystrongpass').html("Password Strength: Very Strong");
             } else if (StrongPass.test(password1.val())) {
                 passwordsInfo.removeClass().addClass('strongpass').html("Password Strength: Strong");
             } else if (MediumPass.test(password1.val())) {
                 passwordsInfo.removeClass().addClass('goodpass').html("Password Strength: Good");
             } else if (WeakPass.test(password1.val())) {
                 passwordsInfo.removeClass().addClass('stillweakpass').html("Password Strength: Weak");
             } else {
                 passwordsInfo.removeClass().addClass('weakpass').html("Password Strength: Very Weak");
             }

         }
     });

 };

 const removeErrorSuccessClass = (element) => {
     if ($(element).hasClass("alert alert-danger")) {
         $(element).removeClass("alert alert-danger").addClass('text-muted');
     } else if ($(element).hasClass("alert alert-success")) {
         $(element).removeClass("alert alert-success").addClass('text-muted');
     }
 };


 $(function() {

     let signupMessage = $("#signup-message");
     let signupButton = $("#signup-submit");
     let signupForm = $("#auth-signup");
     let password1 = $('#password'); //id of first password field
     let password2 = $('#confirm_password'); //id of confirm password field
     let passwordsInfo = $('#pass-info'); //id of indicator element
     let email = $("#email");

     validateEmail(email, passwordsInfo);
     passwordStrengthCheck(password1, passwordsInfo); //call password check function
     passwordEqualityCheck(password1, password2, passwordsInfo);
     removeErrorSuccessClass(signupMessage);

     signupForm.submit(function(event) {
         event.preventDefault();
         $('html, body').animate({
             scrollTop: 0
         }, 'fast');

         let passwordInfo = $('#pass-info');

         passwordInfo.removeClass().html("");

         let formData = {
             'email': $('#email').val(),
             'first_name': $('#first_name').val(),
             'last_name': $('#last_name').val(),
             'gender': $('#gender').val(),
             'type': $('#type').val(),
             'password': $('#password').val(),
             'confirm_password': $('#confirm_password').val(),

         };

         signupButton.attr({
             disabled: true
         });

         removeErrorSuccessClass(signupMessage);
         signupMessage.removeClass();
     });
 });