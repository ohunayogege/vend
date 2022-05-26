$(".login").on("submit", function(e){
    e.preventDefault();
    const username = $("#username").val();
    const password = $("#password").val();
    const fd = $(this);
    if (password === ""){
    Swal.fire({
        position: "top-end",
        icon: "error",
        title: "Please enter password",
        showConfirmButton: !1,
        timer: 1500
    })
    }
    else if (username === ""){
        Swal.fire({
            position: "top-end",
            icon: "error",
            title: "Please enter username",
            showConfirmButton: !1,
            timer: 1500
        })
    }
    else {
        $.ajax({
            url: window.location.href,
            method: 'POST',
            data: fd.serialize(),
            cache: false,
            processData: false,
            beforeSend: function(){
                $(".btnLogin").text("Please Wait...");
                $(".btnLogin").attr("disabled");
            },
            success: function(res){
                if (res.status == true){
                    Swal.fire({
                        position: "center",
                        icon: "success",
                        title: "Login Successful. Please wait for redirection",
                        showConfirmButton: !1,
                        timer: 3000
                    })
                    window.location.reload();
                }
                else{
                    Swal.fire({
                        position: "top-end",
                        icon: "error",
                        title: res.message,
                        showConfirmButton: !1,
                        timer: 3000
                    })
                }
            },
            error: function(){
                Swal.fire({
                    position: "top-end",
                    icon: "error",
                    title: "There was an error. Please try again",
                    showConfirmButton: !1,
                    timer: 3000
                })
            },
            complete: function(){
                $(".btnLogin").text("Log In");
                $(".btnLogin").removeAttr("disabled");
            }
        });
    }
});

