! function (a) {
    "use strict";
    var e, t, n, o = localStorage.getItem("language"),
        r = "en";

    function d(t) {
        document.getElementById("header-lang-img") && ("en" == t ? document.getElementById("header-lang-img").src = "assets/images/flags/us.jpg" : "sp" == t ? document.getElementById("header-lang-img").src = "assets/images/flags/spain.jpg" : "gr" == t ? document.getElementById("header-lang-img").src = "assets/images/flags/germany.jpg" : "it" == t ? document.getElementById("header-lang-img").src = "assets/images/flags/italy.jpg" : "ru" == t && (document.getElementById("header-lang-img").src = "assets/images/flags/russia.jpg"), localStorage.setItem("language", t), null == (o = localStorage.getItem("language")) && d(r), a.getJSON("assets/lang/" + o + ".json", function (t) {
            a("html").attr("lang", o), a.each(t, function (t, e) {
                "head" === t && a(document).attr("title", e.title), a("[data-key='" + t + "']").text(e)
            })
        }))
    }

    function i() {
        var t = document.querySelectorAll(".counter-value");
        t.forEach(function (o) {
            ! function t() {
                var e = +o.getAttribute("data-target"),
                    a = +o.innerText,
                    n = e / 250;
                n < 1 && (n = 1), a < e ? (o.innerText = (a + n).toFixed(0), setTimeout(t, 1)) : o.innerText = e
            }()
        })
    }

    function l() {
        for (var t = document.getElementById("topnav-menu-content").getElementsByTagName("a"), e = 0, a = t.length; e < a; e++) t[e] && t[e].parentElement && "nav-item dropdown active" === t[e].parentElement.getAttribute("class") && (t[e].parentElement.classList.remove("active"), t[e].nextElementSibling && t[e].nextElementSibling.classList.remove("show"))
    }

    // function s(t) {
    //     document.getElementById(t).checked = !0
    // }

    function c() {
        document.webkitIsFullScreen || document.mozFullScreen || document.msFullscreenElement || a("body").removeClass("fullscreen-enable")
    }
    a("#side-menu").metisMenu(), i(), e = document.body.getAttribute("data-sidebar-size"), a(window).on("load", function () {
            a(".switch").on("switch-change", function () {
                toggleWeather()
            }), 1024 <= window.innerWidth && window.innerWidth <= 1366 && (document.body.setAttribute("data-sidebar-size", "sm"))
        }), a("#vertical-menu-btn").on("click", function (t) {
            t.preventDefault(), a("body").toggleClass("sidebar-enable"), 992 <= a(window).width() && (null == e ? null == document.body.getAttribute("data-sidebar-size") || "lg" == document.body.getAttribute("data-sidebar-size") ? document.body.setAttribute("data-sidebar-size", "sm") : document.body.setAttribute("data-sidebar-size", "lg") : "md" == e ? "md" == document.body.getAttribute("data-sidebar-size") ? document.body.setAttribute("data-sidebar-size", "sm") : document.body.setAttribute("data-sidebar-size", "md") : "sm" == document.body.getAttribute("data-sidebar-size") ? document.body.setAttribute("data-sidebar-size", "lg") : document.body.setAttribute("data-sidebar-size", "sm"))
        }), a("#sidebar-menu a").each(function () {
            var t = window.location.href.split(/[?#]/)[0];
            this.href == t && (a(this).addClass("active"), a(this).parent().addClass("mm-active"), a(this).parent().parent().addClass("mm-show"), a(this).parent().parent().prev().addClass("mm-active"), a(this).parent().parent().parent().addClass("mm-active"), a(this).parent().parent().parent().parent().addClass("mm-show"), a(this).parent().parent().parent().parent().parent().addClass("mm-active"))
        }), a(document).ready(function () {
            var t;
            0 < a("#sidebar-menu").length && 0 < a("#sidebar-menu .mm-active .active").length && (300 < (t = a("#sidebar-menu .mm-active .active").offset().top) && (t -= 300, a(".vertical-menu .simplebar-content-wrapper").animate({
                scrollTop: t
            }, "slow")))
        }), a(".navbar-nav a").each(function () {
            var t = window.location.href.split(/[?#]/)[0];
            this.href == t && (a(this).addClass("active"), a(this).parent().addClass("active"), a(this).parent().parent().addClass("active"), a(this).parent().parent().parent().addClass("active"), a(this).parent().parent().parent().parent().addClass("active"), a(this).parent().parent().parent().parent().parent().addClass("active"), a(this).parent().parent().parent().parent().parent().parent().addClass("active"))
        }), a('[data-toggle="fullscreen"]').on("click", function (t) {
            t.preventDefault(), a("body").toggleClass("fullscreen-enable"), document.fullscreenElement || document.mozFullScreenElement || document.webkitFullscreenElement ? document.cancelFullScreen ? document.cancelFullScreen() : document.mozCancelFullScreen ? document.mozCancelFullScreen() : document.webkitCancelFullScreen && document.webkitCancelFullScreen() : document.documentElement.requestFullscreen ? document.documentElement.requestFullscreen() : document.documentElement.mozRequestFullScreen ? document.documentElement.mozRequestFullScreen() : document.documentElement.webkitRequestFullscreen && document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT)
        }), document.addEventListener("fullscreenchange", c), document.addEventListener("webkitfullscreenchange", c), document.addEventListener("mozfullscreenchange", c),
        function () {
            if (document.getElementById("topnav-menu-content")) {
                for (var t = document.getElementById("topnav-menu-content").getElementsByTagName("a"), e = 0, a = t.length; e < a; e++) t[e].onclick = function (t) {
                    t && t.target && "#" === t.target.getAttribute("href") && (t.target.parentElement.classList.toggle("active"), t.target.nextElementSibling && t.target.nextElementSibling.classList.toggle("show"))
                };
                window.addEventListener("resize", l)
            }
        }(), [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]')).map(function (t) {
            return new bootstrap.Tooltip(t)
        }), [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]')).map(function (t) {
            return new bootstrap.Popover(t)
        }), [].slice.call(document.querySelectorAll(".toast")).map(function (t) {
            return new bootstrap.Toast(t)
        }), a(window).on("load", function () {
            a("#status").fadeOut(), a("#preloader").delay(350).fadeOut("slow")
        }), Waves.init(), a("#checkAll").on("change", function () {
            a(".table-check .form-check-input").prop("checked", a(this).prop("checked"))
        }), a(".table-check .form-check-input").change(function () {
            a(".table-check .form-check-input:checked").length == a(".table-check .form-check-input").length ? a("#checkAll").prop("checked", !0) : a("#checkAll").prop("checked", !1)
        })
}(jQuery), feather.replace();

// var myModal = document.getElementById('myModal')
//     var myInput = document.getElementById('myInput')

//     myModal.addEventListener('shown.bs.modal', function () {
//     myInput.focus()
// });

function preview() {
    logo_frame.src = URL.createObjectURL(event.target.files[0]);
}

function clearImage() {
    document.getElementById('logo-image').value = null;
    logo_frame.src = "";
}

function previewIcon() {
    icon_frame.src = URL.createObjectURL(event.target.files[0]);
}

function clearIcon() {
    document.getElementById('icon-image').value = null;
    icon_frame.src = "";
}


function addWallet() {
    const user = $("#user").val();
    var amount = $(".uamount").val();
    var token = $(".csrf").val();
    console.log(amount);

    $.ajax({
        type: "post",
        url: window.location.href,
        data: {
            user: user,
            amount: amount,
            service: 'add'
        },
        dataType: "json",
        headers: {
            "X-CSRFToken": token
        },
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    position: "center",
                    icon: "success",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 5000
                })
                window.location.reload();
            } else {
                Swal.fire({
                    position: "top-end",
                    icon: "error",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 3000
                })
            }

        }
    });
}

function deductWallet() {
    const user = $("#user").val();
    const amount = $(".uamount").val();
    var token = $(".csrf").val();
    console.log(user);


    $.ajax({
        type: "post",
        url: window.location.href,
        data: {
            user: user,
            amount: amount,
            service: 'deduct'
        },
        dataType: "json",
        headers: {
            "X-CSRFToken": token
        },
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    position: "center",
                    icon: "success",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 5000
                })
                window.location.reload();
            } else {
                Swal.fire({
                    position: "top-end",
                    icon: "error",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 3000
                })
            }

        }
    });
}
// Random Pass Gen
function gen_password() {
    var chars = "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&()ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    var passwordLength = 12;
    var password = "";
    for (var i = 0; i <= passwordLength; i++) {
        var randomNumber = Math.floor(Math.random() * chars.length);
        password += chars.substring(randomNumber, randomNumber + 1);
    }
    $(".passwordX").val(password);
    $(".passw").show();
};

function copy_password() {
    var copyText = document.getElementById("passwordX");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value);
};

$(".change_password2").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);

    $.ajax({
        type: "post",
        url: window.location.href,
        data: fd.serialize(),
        dataType: "json",
        processData: false,
        cache: false,
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    type: "success",
                    title: "Success",
                    html: res.message
                })
                window.location.reload();
            } else {
                Swal.fire({
                    type: "error",
                    title: "Error!",
                    html: res.message
                })
            }
        }
    });
});

$(".user_update").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);

    $.ajax({
        type: "post",
        url: window.location.href,
        data: fd.serialize(),
        dataType: "json",
        processData: false,
        cache: false,
        beforeSend: function () {
            $(".update_profile").attr("disabled", "disabled");
            $(".update_profile").text("Loading...");
        },
        complete: function () {
            $(".update_profile").removeAttr("disabled");
            $(".update_profile").text("Update Profile");
        },
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    type: "success",
                    title: "Success",
                    html: res.message
                })
                window.location.reload();
            } else {
                Swal.fire({
                    type: "error",
                    title: "Error!",
                    html: res.message
                })
            }
        }
    });
});


// Website Configuration
$(".upload_image").on("submit", function (e) {
    e.preventDefault();
    const token = $("#csrf").val();
    const logo = $("#logo-image")[0].files[0]
    var fd = new FormData();
    fd.append("logo", logo);
    fd.append("csrfmiddlewaretoken", token);
    $.ajax({
        url: window.location.href,
        method: 'POST',
        data: JSON.stringify(fd),
        headers: {
            "X-CSRFToken": token
        },
        cache: false,
        processData: false,
        beforeSend: function () {
            $(".upload-logo").text("Saving...");
            $(".upload-logo").attr("disabled");
        },
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    position: "center",
                    icon: "success",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 5000
                })
                window.location.reload();
            } else {
                Swal.fire({
                    position: "top-end",
                    icon: "error",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 3000
                })
            }
        },
        error: function () {
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: "There was an error. Please try again",
                showConfirmButton: !1,
                timer: 3000
            })
        },
        complete: function () {
            $(".upload-logo").text("Save Changes");
            $(".upload-logo").removeAttr("disabled");
        }
    });
});

$(".upload_icon").on("submit", function (e) {
    e.preventDefault();
    const token = $("#csrf").val();
    const icon = $("#icon-image")[0].files[0];
    console.log(icon)
    var fd = new FormData(this);
    fd.append("icon", icon);
    fd.append("csrfmiddlewaretoken", token);
    $.ajax({
        url: window.location.href,
        method: 'POST',
        data: JSON.stringify(fd),
        headers: {
            "X-CSRFToken": token
        },
        cache: false,
        processData: false,
        beforeSend: function () {
            $(".upload-icon").text("Saving...");
            $(".upload-icon").attr("disabled");
        },
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    position: "center",
                    icon: "success",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 5000
                })
                window.location.reload();
            } else {
                Swal.fire({
                    position: "top-end",
                    icon: "error",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 3000
                })
            }
        },
        error: function () {
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: "There was an error. Please try again",
                showConfirmButton: !1,
                timer: 3000
            })
        },
        complete: function () {
            $(".upload-icon").text("Save Changes");
            $(".upload-icon").removeAttr("disabled");
        }
    });
});

// Website Configuration
$(".website_config").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);
    $.ajax({
        url: window.location.href,
        method: 'POST',
        data: fd.serialize(),
        cache: false,
        processData: false,
        beforeSend: function () {
            $(".save_config").text("Saving...");
            $(".save_config").attr("disabled");
        },
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    position: "center",
                    icon: "success",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 5000
                })
                window.location.reload();
            } else {
                Swal.fire({
                    position: "top-end",
                    icon: "error",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 3000
                })
            }
        },
        error: function () {
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: "There was an error. Please try again",
                showConfirmButton: !1,
                timer: 3000
            })
        },
        complete: function () {
            $(".save_config").text("Save Changes");
            $(".save_config").removeAttr("disabled");
        }
    });
});

$(".api_setup").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);
    $.ajax({
        url: window.location.href,
        method: 'POST',
        data: fd.serialize(),
        cache: false,
        processData: false,
        beforeSend: function () {
            $(".save_config").text("Saving...");
            $(".save_config").attr("disabled");
        },
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    position: "center",
                    icon: "success",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 5000
                })
                window.location.reload();
            } else {
                Swal.fire({
                    position: "top-end",
                    icon: "error",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 3000
                })
            }
        },
        error: function () {
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: "There was an error. Please try again",
                showConfirmButton: !1,
                timer: 3000
            })
        },
        complete: function () {
            $(".save_config").text("Save Changes");
            $(".save_config").removeAttr("disabled");
        }
    });
});

$(".a2c_setup").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);
    $.ajax({
        url: window.location.href,
        method: 'POST',
        data: fd.serialize(),
        cache: false,
        processData: false,
        beforeSend: function () {
            $(".save_config").text("Saving...");
            $(".save_config").attr("disabled");
        },
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    position: "center",
                    icon: "success",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 5000
                })
                window.location.reload();
            } else {
                Swal.fire({
                    position: "top-end",
                    icon: "error",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 3000
                })
            }
        },
        error: function () {
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: "There was an error. Please try again",
                showConfirmButton: !1,
                timer: 3000
            })
        },
        complete: function () {
            $(".save_config").text("Save Changes");
            $(".save_config").removeAttr("disabled");
        }
    });
});

// Referral
$(".ref_config").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);
    $.ajax({
        url: window.location.href,
        method: 'POST',
        data: fd.serialize(),
        cache: false,
        processData: false,
        beforeSend: function () {
            $(".save_config").text("Saving...");
            $(".save_config").attr("disabled");
        },
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    position: "center",
                    icon: "success",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 5000
                })
                window.location.reload();
            } else {
                Swal.fire({
                    position: "top-end",
                    icon: "error",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 3000
                })
            }
        },
        error: function () {
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: "There was an error. Please try again",
                showConfirmButton: !1,
                timer: 3000
            })
        },
        complete: function () {
            $(".save_config").text("Save Changes");
            $(".save_config").removeAttr("disabled");
        }
    });
});

$(".seo_config").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);
    $.ajax({
        url: window.location.href,
        method: 'POST',
        data: fd.serialize(),
        cache: false,
        processData: false,
        beforeSend: function () {
            $(".save_config").text("Saving...");
            $(".save_config").attr("disabled");
        },
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    position: "center",
                    icon: "success",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 5000
                })
                window.location.reload();
            } else {
                Swal.fire({
                    position: "top-end",
                    icon: "error",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 3000
                })
            }
        },
        error: function () {
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: "There was an error. Please try again",
                showConfirmButton: !1,
                timer: 3000
            })
        },
        complete: function () {
            $(".save_config").text("Save Changes");
            $(".save_config").removeAttr("disabled");
        }
    });
});

$(".data_config").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);
    $.ajax({
        url: window.location.href,
        method: 'POST',
        data: fd.serialize(),
        cache: false,
        processData: false,
        beforeSend: function () {
            $(".save_config").text("Saving...");
            $(".save_config").attr("disabled");
        },
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    position: "center",
                    icon: "success",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 5000
                })
                window.location.reload();
            } else {
                Swal.fire({
                    position: "top-end",
                    icon: "error",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 3000
                })
            }
        },
        error: function () {
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: "There was an error. Please try again",
                showConfirmButton: !1,
                timer: 3000
            })
        },
        complete: function () {
            $(".save_config").text("Save Changes");
            $(".save_config").removeAttr("disabled");
        }
    });
});

$(".airtime_config").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);
    $.ajax({
        url: window.location.href,
        method: 'POST',
        data: fd.serialize(),
        cache: false,
        processData: false,
        beforeSend: function () {
            $(".save_config").text("Saving...");
            $(".save_config").attr("disabled");
        },
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    position: "center",
                    icon: "success",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 5000
                })
                window.location.reload();
            } else {
                Swal.fire({
                    position: "top-end",
                    icon: "error",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 3000
                })
            }
        },
        error: function () {
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: "There was an error. Please try again",
                showConfirmButton: !1,
                timer: 3000
            })
        },
        complete: function () {
            $(".save_config").text("Save Changes");
            $(".save_config").removeAttr("disabled");
        }
    });
});

$(".bills_config").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);
    $.ajax({
        url: window.location.href,
        method: 'POST',
        data: fd.serialize(),
        cache: false,
        processData: false,
        beforeSend: function () {
            $(".save_config").text("Saving...");
            $(".save_config").attr("disabled");
        },
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    position: "center",
                    icon: "success",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 5000
                })
                window.location.reload();
            } else {
                Swal.fire({
                    position: "top-end",
                    icon: "error",
                    title: res.message,
                    showConfirmButton: !1,
                    timer: 3000
                })
            }
        },
        error: function () {
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: "There was an error. Please try again",
                showConfirmButton: !1,
                timer: 3000
            })
        },
        complete: function () {
            $(".save_config").text("Save Changes");
            $(".save_config").removeAttr("disabled");
        }
    });
});

// E-Pins
$(".e_pin").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);

    $.ajax({
        type: "post",
        url: window.location.href,
        data: fd.serialize(),
        dataType: "json",
        processData: false,
        cache: false,
        beforeSend: function () {
            $(".addPin").text("Adding...");
            $(".addPin").attr("disabled", "disabled");
        },
        complete: function () {
            $(".addPin").html("Add Pin<sup>s</sup>");
            $(".addPin").removeAttr("disabled");
        },
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    title: "Success",
                    html: res.message
                })
                window.location.reload();
            } else {
                Swal.fire({
                    title: "Error!",
                    html: res.message
                })
            }
        },
        error: function (err) {
            Swal.fire({
                title: "Error!",
                html: "There was an error. Please try again later."
            })
        }
    });
});
$(".e_airtime").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);

    $.ajax({
        type: "post",
        url: window.location.href,
        data: fd.serialize(),
        dataType: "json",
        processData: false,
        cache: false,
        beforeSend: function () {
            $(".addPin").text("Adding...");
            $(".addPin").attr("disabled", "disabled");
        },
        complete: function () {
            $(".addPin").html("Add Pin<sup>s</sup>");
            $(".addPin").removeAttr("disabled");
        },
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    type: "success",
                    title: "Success",
                    html: res.message
                })
                window.location.reload();
            } else {
                Swal.fire({
                    type: "error",
                    title: "Error!",
                    html: res.message
                })
            }
        }
    });
});

$(".pin_config").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);

    $.ajax({
        type: "post",
        url: window.location.href,
        data: fd.serialize(),
        dataType: "json",
        processData: false,
        cache: false,
        beforeSend: function () {
            $(".save_config").text("Saving...");
            $(".save_config").attr("disabled", "disabled");
        },
        complete: function () {
            $(".save_config").html("Save Changes");
            $(".save_config").removeAttr("disabled");
        },
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    title: "Success",
                    html: res.message
                })
                window.location.reload();
            } else {
                Swal.fire({
                    title: "Error!",
                    html: res.message
                })
            }
        },
        error: function (err) {
            Swal.fire({
                title: "Error!",
                html: "There was an error. Please try again later."
            })
        }
    });
});

function deleteCard(status) {
    console.log(status);
    $.ajax({
        type: "get",
        url: window.location.href,
        data: {
            card_type: status
        },
        dataType: "json",
        success: function (res) {
            Swal.fire({
                title: "Success",
                html: res.message
            })
            window.location.reload();
        },
        error: function (err) {
            console.log(err);
            Swal.fire({
                title: "Error!",
                html: "There was an error. Please try again later."
            })
        }
    });
};

$(".add_staff").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);

    $.ajax({
        type: "post",
        url: window.location.href,
        data: fd.serialize(),
        dataType: "json",
        processData: false,
        cache: false,
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    type: "success",
                    title: "Success",
                    html: res.message
                })
                window.location.reload();
            } else {
                Swal.fire({
                    type: "error",
                    title: "Error!",
                    html: res.message
                })
            }
        }
    });
});

$(".announcementNew").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);

    $.ajax({
        type: "post",
        url: window.location.href,
        data: fd.serialize(),
        dataType: "json",
        processData: false,
        cache: false,
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    type: "success",
                    title: "Success",
                    html: res.message
                })
                window.location.reload();
            } else {
                Swal.fire({
                    type: "error",
                    title: "Error!",
                    html: res.message
                })
            }
        }
    });
});

$(function () {
    var e = {};
    $(".table-edits tr").editable({
        dropdowns: {
            active: ["True", "False"]
        },
        edit: function (t) {
            $(".edit i", this).removeClass("fa-pencil-alt").addClass("fa-save").attr("title", "Save")
        },
        save: function (t) {
            const datas = JSON.stringify(t);
            const data = JSON.parse(datas);
            $.ajax({
                type: "get",
                url: window.location.href,
                data: {
                    slug: data.slug,
                    id:data.id,
                    network:data.network,
                    active:data.active
                },
                dataType: "JSON",
                success: function (res) {
                    if (res.status == true) {
                        Swal.fire({
                            title: "Success",
                            html: res.message
                        })
                    } else {
                        Swal.fire({
                            type: "error",
                            title: "Error!",
                            html: res.message
                        })
                    }
                }
            });
            $(".edit i", this).removeClass("fa-save").addClass("fa-pencil-alt").attr("title", "Edit"), this in e && (e[this].destroy(), delete e[this])
        },
        cancel: function (t) {
            $(".edit i", this).removeClass("fa-save").addClass("fa-pencil-alt").attr("title", "Edit"), this in e && (e[this].destroy(), delete e[this])
        }
    })
});

$(function () {
    var e = {};
    $(".table-edits2 tr").editable({
        dropdowns: {
            active: ["True", "False"]
        },
        edit: function (t) {
            $(".edit i", this).removeClass("fa-pencil-alt").addClass("fa-save").attr("title", "Save")
        },
        save: function (t) {
            const datas = JSON.stringify(t);
            const data = JSON.parse(datas);
            $.ajax({
                type: "get",
                url: window.location.href,
                data: data,
                dataType: "JSON",
                success: function (res) {
                    if (res.status == true) {
                        Swal.fire({
                            title: "Success",
                            html: res.message
                        })
                    } else {
                        Swal.fire({
                            type: "error",
                            title: "Error!",
                            html: res.message
                        })
                    }
                }
            });
            $(".edit i", this).removeClass("fa-save").addClass("fa-pencil-alt").attr("title", "Edit"), this in e && (e[this].destroy(), delete e[this])
        },
        cancel: function (t) {
            $(".edit i", this).removeClass("fa-save").addClass("fa-pencil-alt").attr("title", "Edit"), this in e && (e[this].destroy(), delete e[this])
        }
    })
});

$(function () {
    var e = {};
    $(".table-edits3 tr").editable({
        dropdowns: {
            active: ["True", "False"]
        },
        edit: function (t) {
            $(".edit i", this).removeClass("fa-pencil-alt").addClass("fa-save").attr("title", "Save")
        },
        save: function (t) {
            const datas = JSON.stringify(t);
            const data = JSON.parse(datas);
            $.ajax({
                type: "get",
                url: window.location.href,
                data: data,
                dataType: "JSON",
                success: function (res) {
                    if (res.status == true) {
                        Swal.fire({
                            title: "Success",
                            html: res.message
                        })
                    } else {
                        Swal.fire({
                            type: "error",
                            title: "Error!",
                            html: res.message
                        })
                    }
                }
            });
            $(".edit i", this).removeClass("fa-save").addClass("fa-pencil-alt").attr("title", "Edit"), this in e && (e[this].destroy(), delete e[this])
        },
        cancel: function (t) {
            $(".edit i", this).removeClass("fa-save").addClass("fa-pencil-alt").attr("title", "Edit"), this in e && (e[this].destroy(), delete e[this])
        }
    })
});

$(function () {
    var e = {};
    $(".table-edits4 tr").editable({
        dropdowns: {
            active: ["True", "False"]
        },
        edit: function (t) {
            $(".edit i", this).removeClass("fa-pencil-alt").addClass("fa-save").attr("title", "Save")
        },
        save: function (t) {
            const datas = JSON.stringify(t);
            const data = JSON.parse(datas);
            $.ajax({
                type: "get",
                url: window.location.href,
                data: {
                    plan: data.plan,
                    pid:data.pid,
                    decoder:data.decoder,
                    customer_price: data.customer_price,
                    reseller_price: data.reseller_price,
                    api_price: data.api_price,
                    active:data.active
                },
                dataType: "JSON",
                success: function (res) {
                    if (res.status == true) {
                        Swal.fire({
                            title: "Success",
                            html: res.message
                        })
                    } else {
                        Swal.fire({
                            type: "error",
                            title: "Error!",
                            html: res.message
                        })
                    }
                }
            });
            $(".edit i", this).removeClass("fa-save").addClass("fa-pencil-alt").attr("title", "Edit"), this in e && (e[this].destroy(), delete e[this])
        },
        cancel: function (t) {
            $(".edit i", this).removeClass("fa-save").addClass("fa-pencil-alt").attr("title", "Edit"), this in e && (e[this].destroy(), delete e[this])
        }
    })
});

$(".product_config").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);

    $.ajax({
        type: "post",
        url: window.location.href,
        data: fd.serialize(),
        dataType: "json",
        processData: false,
        cache: false,
        success: function (res) {
            if (res.status == true) {
                Swal.fire({
                    type: "success",
                    title: "Success",
                    html: res.message
                })
                window.location.reload();
            } else {
                Swal.fire({
                    type: "error",
                    title: "Error!",
                    html: res.message
                })
            }
        }
    });
});