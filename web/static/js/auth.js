$(".login").on("submit", function(e){
    e.preventDefault();
    const fd = $(this);
    const username = $(".username").val();

    $.ajax({
        type: "post",
        url: window.location.href,
        data: fd.serialize(),
        dataType: "json",
        cache: false,
        processData: false,
        beforeSend: function(){
            $(".login-btn").attr("disabled", "disabled");
            $(".login-btn").text("Please Wait...");
        },
        success: function (res) {
            if (res.status==true){
                $('.login').find('.alert').removeClass('alert-warning');
                $('.login').find('.alert').removeClass('none');
                $('.login').find('.alert').addClass('alert-success');
                $('#output').html(res.message) /* response message */
                // if (localStorage.getItem("userAccount") === null) {
                //     localStorage.setItem("userAccount", username);
                // }
                setTimeout(window.location.reload(), 5000);
            }else {
                $('.login').find('.alert').removeClass('alert-success');
                $('.login').find('.alert').removeClass('none');
                $('.login').find('.alert').addClass('alert-warning');
                $('#output').html(res.message) /* response message */
            }
        },
        error: function(err){
            $('.login').find('.alert').removeClass('alert-success');
            $('.login').find('.alert').removeClass('none');
            $('.login').find('.alert').addClass('alert-warning');
            $('#output').html(err.status+' - '+err.statusText+': There was an error with the server. Please try again later.') /* response message */
        },
        complete: function(){
            $(".login-btn").removeAttr("disabled");
            $(".login-btn").text("Log In");
        }
    });
});

$(".register").on("submit", function(e){
    e.preventDefault();
    const fd = $(this);

    $.ajax({
        type: "post",
        url: window.location.href,
        data: fd.serialize(),
        dataType: "json",
        cache: false,
        processData: false,
        beforeSend: function(){
            $(".register-btn").attr("disabled", "disabled");
            $(".register-btn").text("Please Wait...");
        },
        success: function (res) {
            if (res.status==true){
                $('.register').find('.alert').removeClass('alert-warning');
                $('.register').find('.alert').removeClass('none');
                $('.register').find('.alert').addClass('alert-success');
                $('#output').html(res.message) /* response message */
                setTimeout(window.location.href="/login/", 5000);
            }else {
                $('.register').find('.alert').removeClass('alert-success');
                $('.register').find('.alert').removeClass('none');
                $('.register').find('.alert').addClass('alert-warning');
                $('#output').html(res.message) /* response message */
            }
            
        },
        error: function(err){
            $('.register').find('.alert').removeClass('alert-success');
            $('.register').find('.alert').removeClass('none');
            $('.register').find('.alert').addClass('alert-warning');
            $('#output').html(err.status+' - '+err.statusText+': There was an error with the server. Please try again later.') /* response message */
        },
        complete: function(){
            $(".register-btn").removeAttr("disabled");
            $(".register-btn").text("Register");
        }
    });
});

$(document).ready(function () {  
    $('#password').keyup(function () {  
        $('#strengthMessage').html(checkStrength($('#password').val()))  
    });
    $("#cpassword").keyup(function () {
        $('#matchMessage').html(checkPasswordMatch($('#cpassword').val()))});

    function checkStrength(password) {  
        var strength = 0 
        if (password.length < 7) {  
            $('#strengthMessage').removeClass()  
            $('#strengthMessage').addClass('Short')
            return 'Password too short'
        }
        if (password.length > 7) strength += 1  
        // If password contains both lower and uppercase characters, increase strength value.  
        if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) strength += 1
        // If it has numbers and characters, increase strength value.  
        if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/)) strength += 1
        // If it has one special character, increase strength value.  
        if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1
        // If it has two special characters, increase strength value.  
        if (password.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1
        // Calculated strength value, we can return messages  
        // If value is less than 2  
        if (strength < 2) {
            $('#strengthMessage').removeClass()
            $('#strengthMessage').addClass('Weak') 
            return 'Weak'  
        } else if (strength == 2) {  
            $('#strengthMessage').removeClass()  
            $('#strengthMessage').addClass('Good')  
            return 'Good'  
        } else {  
            $('#strengthMessage').removeClass()  
            $('#strengthMessage').addClass('Strong')  
            return 'Strong'  
        }
    }

    function checkPasswordMatch() {
        var password = $("#password").val();
        var confirmPassword = $("#cpassword").val();

        if (confirmPassword.length < 7) {
            $('#matchMessage').removeClass();
            $('#matchMessage').addClass('Short');
            $("#regBtn").attr("disabled", "disabled");
            return 'Password is too short';
        }
        else if (password != confirmPassword) {
            $('#matchMessage').removeClass();
            $('#matchMessage').addClass('NotMatch');
            $("#regBtn").attr("disabled", "disabled");
            return 'Passwords does not match';
        }
        else {
            $('#matchMessage').removeClass();
            $('#matchMessage').addClass('Match');
            $("#regBtn").removeAttr("disabled");
            return 'Passwords matched'; 
        }
    }
});

$(".verify").on("submit", function(e){
    e.preventDefault();
    const fd = $(this);

    $.ajax({
        type: "post",
        url: window.location.href,
        data: fd.serialize(),
        dataType: "json",
        cache: false,
        processData: false,
        beforeSend: function(){
            $(".verify-btn").attr("disabled", "disabled");
            $(".verify-btn").text("Please Wait...");
        },
        success: function (res) {
            if (res.status==true){
                $('.verify').find('.alert').removeClass('alert-warning');
                $('.verify').find('.alert').removeClass('none');
                $('.verify').find('.alert').addClass('alert-success');
                $('#output').html(res.message) /* response message */
                setTimeout(window.location.href="/login/", 5000);
            }else {
                $('.verify').find('.alert').removeClass('alert-success');
                $('.verify').find('.alert').removeClass('none');
                $('.verify').find('.alert').addClass('alert-warning');
                $('#output').html(res.message) /* response message */
            }
            
        },
        error: function(err){
            $('.verify').find('.alert').removeClass('alert-success');
            $('.verify').find('.alert').removeClass('none');
            $('.verify').find('.alert').addClass('alert-warning');
            $('#output').html(err.status+' - '+err.statusText+': There was an error with the server. Please try again later.') /* response message */
        },
        complete: function(){
            $(".verify-btn").removeAttr("disabled");
            $(".verify-btn").text("Verify Now");
        }
    });
});

$(".fpassword").on("submit", function(e){
    e.preventDefault();
    const fd = $(this);

    $.ajax({
        type: "post",
        url: window.location.href,
        data: fd.serialize(),
        dataType: "json",
        cache: false,
        processData: false,
        beforeSend: function(){
            $(".verify-btn").attr("disabled", "disabled");
            $(".verify-btn").text("Please Wait...");
        },
        success: function (res) {
            if (res.status==true){
                $('.fpassword').find('.alert').removeClass('alert-warning');
                $('.fpassword').find('.alert').removeClass('none');
                $('.fpassword').find('.alert').addClass('alert-success');
                $('#output').html(res.message) /* response message */
                setTimeout(window.location.href="/reset-password/", 5000);
            }else {
                $('.fpassword').find('.alert').removeClass('alert-success');
                $('.fpassword').find('.alert').removeClass('none');
                $('.fpassword').find('.alert').addClass('alert-warning');
                $('#output').html(res.message) /* response message */
            }
            
        },
        error: function(err){
            $('.fpassword').find('.alert').removeClass('alert-success');
            $('.fpassword').find('.alert').removeClass('none');
            $('.fpassword').find('.alert').addClass('alert-warning');
            $('#output').html(err.status+' - '+err.statusText+': There was an error with the server. Please try again later.') /* response message */
        },
        complete: function(){
            $(".verify-btn").removeAttr("disabled");
            $(".verify-btn").text("Proceed");
        }
    });
});

$(".rpassword").on("submit", function(e){
    e.preventDefault();
    const fd = $(this);

    $.ajax({
        type: "post",
        url: window.location.href,
        data: fd.serialize(),
        dataType: "json",
        cache: false,
        processData: false,
        beforeSend: function(){
            $(".verify-btn").attr("disabled", "disabled");
            $(".verify-btn").text("Please Wait...");
        },
        success: function (res) {
            if (res.status==true){
                $('.rpassword').find('.alert').removeClass('alert-warning');
                $('.rpassword').find('.alert').removeClass('none');
                $('.rpassword').find('.alert').addClass('alert-success');
                $('#output').html(res.message) /* response message */
                setTimeout(window.location.href="/login/", 5000);
            }else {
                $('.rpassword').find('.alert').removeClass('alert-success');
                $('.rpassword').find('.alert').removeClass('none');
                $('.rpassword').find('.alert').addClass('alert-warning');
                $('#output').html(res.message) /* response message */
            }
            
        },
        error: function(err){
            $('.rpassword').find('.alert').removeClass('alert-success');
            $('.rpassword').find('.alert').removeClass('none');
            $('.rpassword').find('.alert').addClass('alert-warning');
            $('#output').html(err.status+' - '+err.statusText+': There was an error with the server. Please try again later.') /* response message */
        },
        complete: function(){
            $(".verify-btn").removeAttr("disabled");
            $(".verify-btn").text("Reset Password");
        }
    });
});

