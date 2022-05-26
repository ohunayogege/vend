! function (t) {
    "use strict";

    function s(e) {
        1 == t("#light-mode-switch").prop("checked") && "light-mode-switch" === e ? (t("#dark-mode-switch").prop("checked", !1), t("#rtl-mode-switch").prop("checked", !1), t("#bootstrap-style").attr("href", "assets/css/bootstrap.min.css"), t("#app-style").attr("href", "assets/css/app.min.css"), sessionStorage.setItem("is_visited", "light-mode-switch")) : 1 == t("#dark-mode-switch").prop("checked") && "dark-mode-switch" === e ? (t("#light-mode-switch").prop("checked", !1), t("#rtl-mode-switch").prop("checked", !1), t("#bootstrap-style").attr("href", "assets/css/bootstrap-dark.min.css"), t("#app-style").attr("href", "assets/css/app-dark.min.css"), sessionStorage.setItem("is_visited", "dark-mode-switch")) : 1 == t("#rtl-mode-switch").prop("checked") && "rtl-mode-switch" === e && (t("#light-mode-switch").prop("checked", !1), t("#dark-mode-switch").prop("checked", !1), t("#bootstrap-style").attr("href", "assets/css/bootstrap.min.css"), t("#app-style").attr("href", "assets/css/app-rtl.min.css"), sessionStorage.setItem("is_visited", "rtl-mode-switch"))
    }

    function e() {
        document.webkitIsFullScreen || document.mozFullScreen || document.msFullscreenElement || (console.log("pressed"), t("body").removeClass("fullscreen-enable"))
    }
    t("#side-menu").metisMenu(), t("#vertical-menu-btn").on("click", function (e) {
            e.preventDefault(), t("body").toggleClass("sidebar-enable"), 992 <= t(window).width() ? t("body").toggleClass("vertical-collpsed") : t("body").removeClass("vertical-collpsed")
        }), t("#sidebar-menu a").each(function () {
            var e = window.location.href.split(/[?#]/)[0];
            this.href == e && (t(this).addClass("active"), t(this).parent().addClass("mm-active"), t(this).parent().parent().addClass("mm-show"), t(this).parent().parent().prev().addClass("mm-active"), t(this).parent().parent().parent().addClass("mm-active"), t(this).parent().parent().parent().parent().addClass("mm-show"), t(this).parent().parent().parent().parent().parent().addClass("mm-active"))
        }), t(".navbar-nav a").each(function () {
            var e = window.location.href.split(/[?#]/)[0];
            this.href == e && (t(this).addClass("active"), t(this).parent().addClass("active"), t(this).parent().parent().addClass("active"), t(this).parent().parent().parent().addClass("active"), t(this).parent().parent().parent().parent().addClass("active"))
        }), t('[data-toggle="fullscreen"]').on("click", function (e) {
            e.preventDefault(), t("body").toggleClass("fullscreen-enable"), document.fullscreenElement || document.mozFullScreenElement || document.webkitFullscreenElement ? document.cancelFullScreen ? document.cancelFullScreen() : document.mozCancelFullScreen ? document.mozCancelFullScreen() : document.webkitCancelFullScreen && document.webkitCancelFullScreen() : document.documentElement.requestFullscreen ? document.documentElement.requestFullscreen() : document.documentElement.mozRequestFullScreen ? document.documentElement.mozRequestFullScreen() : document.documentElement.webkitRequestFullscreen && document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT)
        }), document.addEventListener("fullscreenchange", e), document.addEventListener("webkitfullscreenchange", e), document.addEventListener("mozfullscreenchange", e), t(".right-bar-toggle").on("click", function (e) {
            t("body").toggleClass("right-bar-enabled")
        }), t(document).on("click", "body", function (e) {
            0 < t(e.target).closest(".right-bar-toggle, .right-bar").length || t("body").removeClass("right-bar-enabled")
        }), t(".dropdown-menu a.dropdown-toggle").on("click", function (e) {
            return t(this).next().hasClass("show") || t(this).parents(".dropdown-menu").first().find(".show").removeClass("show"), t(this).next(".dropdown-menu").toggleClass("show"), !1
        }), t(function () {
            t('[data-toggle="tooltip"]').tooltip()
        }), t(function () {
            t('[data-toggle="popover"]').popover()
        }),
        function () {
            if (window.sessionStorage) {
                var e = sessionStorage.getItem("is_visited");
                e ? (t(".right-bar input:checkbox").prop("checked", !1), t("#" + e).prop("checked", !0), s(e)) : sessionStorage.setItem("is_visited", "light-mode-switch")
            }
        }(), t(window).on("load", function () {
            t("#status").fadeOut(), t("#preloader").delay(350).fadeOut("slow")
        }), Waves.init()
}(jQuery);

function copyLink() {
    var copyText = document.getElementById("refLink");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(copyText.value);
  
  var tooltip = document.getElementById("myTooltipc");
  tooltip.innerHTML = "Copied: " + copyText.value;
  }

  function outFunc() {
    var tooltip = document.getElementById("myTooltipc");
    tooltip.innerHTML = "Copy to clipboard";
  }

$("#transaction_pin").on("submit", function (e) {
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

$("#change_password").on("submit", function (e) {
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

$("#payfund").on("submit", function (e) {
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
                console.log(res.data)
                MonnifySDK.initialize({
                    amount: res.data.amount,
                    currency: "NGN",
                    reference: res.data.ref,
                    customerName: res.data.customer,
                    customerEmail: res.data.email,
                    apiKey: res.data.api,
                    contractCode: res.data.contract,
                    paymentDescription: "Wallet Funding",
                    isTestMode: false,
                    paymentMethods: ["CARD"],
                    onComplete: function (response) {
                        //Implement what happens when transaction is completed.
                        console.log(response);
                        if (response.requestSuccessful == false) {
                            $.ajax({
                                type: "get",
                                url: "/fund-wallet/confirm/",
                                data: {ref: res.data.ref, "status": 'failed'},
                                dataType: "json",
                                success: function (r) {
                                    // window.location.reload();
                                    console.log("///////////////////////////////////////////////");
                                }
                            });
                        }
                        // {
                        //     accountReference: null
                        //     amountPaid: "5000.00"
                        //     invoiceReference: null
                        //     paidOn: "26/08/2019 02:13:32"
                        //     paymentDescription: "Test Pay"
                        //     paymentReference: "421168696"
                        //     paymentStatus: "PAID"
                        //     totalPayable: "5000.00"
                        //     transactionHash: "6373d5039175201eed06c1872c557749cfba27f0d56d75ff713e58f06ebad84795d38b34334ca59470ffae8addfbdf113ec36823a1607325c89da4981e1054bf"
                        //     transactionReference: "MNFY|20190826141314|000290"
                        // }
                    },
                    onClose: function (data) {
                        //Implement what should happen when the modal is closed here
                        $.ajax({
                            type: "get",
                            url: "/fund-wallet/confirm/",
                            data: {ref: res.data.ref, "status": 'closed'},
                            dataType: "json",
                            success: function (r) {
                                // window.location.reload();
                                console.log("///////////////////////////////////////////////");
                            }
                        });
                    }
                });
            }
        }
    });
});
// Data Plan
$(".network").on("change", function () {
    const selected = $(".network").find(":selected").val();

    $.ajax({
        type: "get",
        url: window.location.href,
        data: {
            network: selected,
            service: 'package'
        },
        dataType: "json",
        success: function (res) {
            $(".package-selection").show();
            let dropdown = $('.package');

            dropdown.empty();

            dropdown.append('<option selected="true" disabled>Select Package</option>');
            dropdown.prop('selectedIndex', 0);

            $.each(res.data, function (key, entry) {
                dropdown.append($('<option></option>').attr('value', entry.id).attr('data-amount', entry.price).text(entry.name));
            });
        }
    });
});

$(".package").on("change", function () {
    const selected = $(".package").find(":selected").data("amount");
    $(".amount").val(`₦${selected}`);
});
$(".dataPlan").on("submit", function (e) {
    e.preventDefault();
    const user_pin = $(".user_inp").val();
    const fd = $(this);

    Swal.fire({
        title: "Enter Transaction Pin",
        input: "password",
        showCancelButton: !0,
        confirmButtonText: "Submit",
        showLoaderOnConfirm: !0,
        confirmButtonColor: "#556ee6",
        cancelButtonColor: "#f46a6a",
        preConfirm: function (n) {
            return new Promise(function (t, e) {
                if (user_pin !== n) {
                    Swal.fire({
                        type: "error",
                        title: "Error!",
                        html: "Incorrect Transaction Pin"
                    })
                } else {
                    $.ajax({
                        type: "get",
                        url: window.location.href,
                        data: fd.serialize(),
                        dataType: "json",
                        success: function (res) {
                            if (res.status == true) {
                                Swal.fire({
                                    type: "success",
                                    title: "Successful",
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
                }
            })
        },
        allowOutsideClick: !1
    })
});

// Airtime
$(".mobile").on("keyup", function () {
    const selected = $(".network").find(":selected").val();
    const mobile = $(".mobile").val();

    $.ajax({
        type: "get",
        url: window.location.href,
        data: {
            network: selected,
            service: 'check',
            mobile: mobile
        },
        dataType: "json",
        success: function (res) {
            if (res.status == false){
                var errorDiv = document.getElementById("errorNumber");
                errorDiv.innerHTML = "The Number does not match with the network. If you continue, it means you have ported the number.";
                errorDiv.classList.remove("valid");												
                errorDiv.classList.add("invalid");
            } else {
                var errorDiv = document.getElementById("errorNumber");
                errorDiv.innerHTML = "The Number is Valid.";
                errorDiv.classList.remove("invalid");				
                errorDiv.classList.add("valid");
            }
        }
    });
});

$(".airtime").on("submit", function (e) {
    e.preventDefault();
    const user_pin = $(".user_inp").val();
    const fd = $(this);

    Swal.fire({
        title: "Enter Transaction Pin",
        input: "password",
        showCancelButton: !0,
        confirmButtonText: "Submit",
        showLoaderOnConfirm: !0,
        confirmButtonColor: "#556ee6",
        cancelButtonColor: "#f46a6a",
        preConfirm: function (n) {
            return new Promise(function (t, e) {
                if (user_pin !== n) {
                    Swal.fire({
                        type: "error",
                        title: "Error!",
                        html: "Incorrect Transaction Pin"
                    })
                } else {
                    $.ajax({
                        type: "get",
                        url: window.location.href,
                        data: fd.serialize(),
                        dataType: "json",
                        success: function (res) {
                            if (res.status == true) {
                                Swal.fire({
                                    type: "success",
                                    title: "Successful",
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
                }
            })
        },
        allowOutsideClick: !1
    })
});


$(".decoder").on("change", function () {
    const selected = $(".decoder").find(":selected").val();

    $.ajax({
        type: "get",
        url: window.location.href,
        data: {
            decoder: selected,
            service: 'package'
        },
        dataType: "json",
        success: function (res) {
            $(".package-selection").show();
            $(".iuc-selection").show();
            $(".cphone-selection").show();
            let dropdown = $('.package');

            dropdown.empty();

            dropdown.append('<option selected="true" disabled>Select Package</option>');
            dropdown.prop('selectedIndex', 0);

            $.each(res.data.varations, function (key, entry) {
                dropdown.append($('<option></option>').attr('value', entry.variation_code).attr('data-amount', entry.variation_amount).text(entry.name));
            });
        }
    });
});
$(".package").on("change", function () {
    const selected = $(".package").find(":selected").data("amount");
    $("#amount").val(selected);
});

$("#decoder_tv").on("submit", function (e) {
    e.preventDefault();
    const iuc = $(".smart_card").val();
    const selected = $(".decoder").find(":selected").val();
    $.ajax({
        type: "get",
        url: window.location.href,
        data: {
            decoder: selected,
            service: 'validate',
            iuc: iuc
        },
        dataType: "json",
        success: function (res) {
            $(".cname-selection").show();
            $(".cname").val(res.data.Customer_Name);
            $('#decoder_tv select').attr('disabled', 'disabled');
            $('#decoder_tv input').attr('readonly', 'readonly');
            $(".validate").hide();
            $(".purchase").show();
        }
    });
});

function purchaseTV() {
    const user_pin = $(".user_inp").val();
    const decoder = $(".decoder").find(":selected").val();
    const package = $(".package").find(":selected").val();
    const iuc = $(".smart_card").val();
    const cname = $(".cname").val();
    const cphone = $(".cphone").val();
    const amount = $("#amount").val();

    Swal.fire({
        title: "Enter Transaction Pin",
        input: "password",
        showCancelButton: !0,
        confirmButtonText: "Submit",
        showLoaderOnConfirm: !0,
        confirmButtonColor: "#556ee6",
        cancelButtonColor: "#f46a6a",
        preConfirm: function (n) {
            return new Promise(function (t, e) {
                if (user_pin !== n) {
                    Swal.fire({
                        type: "error",
                        title: "Error!",
                        html: "Incorrect Transaction Pin"
                    })
                } else {
                    $.ajax({
                        type: "get",
                        url: window.location.href,
                        data: {
                            service: 'purchase',
                            decoder: decoder,
                            package: package,
                            iuc: iuc,
                            cname: cname,
                            cphone: cphone,
                            amount: amount
                        },
                        dataType: "json",
                        success: function (res) {
                            if (res.status == true) {
                                Swal.fire({
                                    type: "success",
                                    title: "Successful",
                                    html: "Successfully Purchased."
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
                }
            })
        },
        allowOutsideClick: !1
    })
}

$(".discotype").change(function () {
    const discotype = $(".discotype").find(":selected").val();
    if (discotype == "") {
        $("#img_loader").html("");
    } else if (discotype == "abuja-electric") {
        $("#img_loader").html("<img class='img-fluid' src='/static/images/abuja.png' height='50' width='50' style='border-radius:50px;'>");
    } else if (discotype == "ibadan-electric") {
        $("#img_loader").html("<img class='img-fluid' src='/static/images/ibadan.png' height='50' width='50' style='border-radius:50px;'>");
    } else if (discotype == "eko-electric") {
        $("#img_loader").html("<img class='img-fluid' src='/static/images/eko.png' height='50' width='50' style='border-radius:50px;'>");
    } else if (discotype == "ikeja-electric") {
        $("#img_loader").html("<img class='img-fluid' src='/static/images/ikeja.png' height='50' width='50' style='border-radius:50px;'>");
    } else if (discotype == "jos-electric") {
        $("#img_loader").html("<img class='img-fluid' src='/static/images/jos.png' height='50' width='50' style='border-radius:50px;'>");
    } else if (discotype == "kaduna-electric") {
        $("#img_loader").html("<img class='img-fluid' src='/static/images/kaduna.png' height='50' width='50' style='border-radius:50px;'>");
    } else if (discotype == "kano-electric") {
        $("#img_loader").html("<img class='img-fluid' src='/static/images/kano.png' height='50' width='50' style='border-radius:50px;'>");
    } else if (discotype == "portharcourt-electric") {
        $("#img_loader").html("<img class='img-fluid' src='/static/images/portharcourt.png' height='50' width='50' style='border-radius:50px;'>");
    } else {
        $("#img_loader").html("");
    }
})

$("#metet").on("submit", function (e) {
    e.preventDefault();
    const iuc = $(".disco_number").val();
    const selected = $(".discotype").find(":selected").val();
    const selected_plan = $(".disco_type").find(":selected").val();
    $.ajax({
        type: "get",
        url: window.location.href,
        data: {
            disco: selected,
            disco_type: selected_plan,
            service: 'validate',
            iuc: iuc
        },
        dataType: "json",
        success: function (res) {
            $(".cname-selection").show();
            $(".cname").val(res.data.Customer_Name);
            $('#metet select').attr('disabled', 'disabled');
            $('#metet input').attr('readonly', 'readonly');
            $(".validate").hide();
            $(".purchase").show();
        }
    });
});

function purchaseToken() {
    const user_pin = $(".user_inp").val();
    const decoder = $(".discotype").find(":selected").val();
    const package = $(".disco_type").find(":selected").val();
    const iuc = $(".mobile_number").val();
    const cname = $(".disco_number").val();
    const cphone = $(".cphone").val();
    const amount = $(".amount").val();

    Swal.fire({
        title: "Enter Transaction Pin",
        input: "password",
        showCancelButton: !0,
        confirmButtonText: "Submit",
        showLoaderOnConfirm: !0,
        confirmButtonColor: "#556ee6",
        cancelButtonColor: "#f46a6a",
        preConfirm: function (n) {
            return new Promise(function (t, e) {
                if (user_pin !== n) {
                    Swal.fire({
                        type: "error",
                        title: "Error!",
                        html: "Incorrect Transaction Pin"
                    })
                } else {
                    $.ajax({
                        type: "get",
                        url: window.location.href,
                        data: {
                            service: 'purchase',
                            decoder: decoder,
                            package: package,
                            iuc: iuc,
                            cname: cname,
                            cphone: cphone,
                            amount: amount
                        },
                        dataType: "json",
                        success: function (res) {
                            if (res.status == true) {
                                Swal.fire({
                                    type: "success",
                                    title: "Successful",
                                    html: "Successfully Purchased."
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
                }
            })
        },
        allowOutsideClick: !1
    })
}

$(".smilePlan").on("change", function () {
    $(".amount").val($(".smilePlan").find(":selected").data("amount"));
});

$("#smile").on("submit", function (e) {
    e.preventDefault();
    const mobile_number = $(".mobile_number").val();
    $.ajax({
        type: "get",
        url: window.location.href,
        data: {
            mobile_number: mobile_number,
            service: 'validate'
        },
        dataType: "json",
        success: function (res) {
            $(".cname-selection").show();
            $(".cname").val(res.data.Customer_Name);
            $('#smile select').attr('disabled', 'disabled');
            $('#smile input').attr('readonly', 'readonly');
            $(".validate").hide();
            $(".purchase").show();
        }
    });
});

$(".bank").on("change", function () {
    const slug = $(".bank").find(":selected").data("slug");
    $("#img_loader").html(`<img class='img-fluid' src='/static/images/logos/${slug}.png' height='50' width='50' style='border-radius:50px;'>`);
});

$(".account_number").on("keyup", function () {
    const account_Number = $(".account_number").val();
    const bank = $(".bank").find(":selected").data("code");
    if (account_Number.length == 10) {
        $(".account_number").attr("disabled", "disabled"),
            $.ajax({
                type: "GET",
                url: "/fetchNuban/",
                data: {
                    bank_code: bank,
                    account_number: account_Number
                },
                dataType: "json",
                success: function (res) {
                    $(".account_name").val(res.data.account_name);
                    $(".account_number").removeAttr("disabled");
                },
                error: function () {
                    $(".account_number").removeAttr("disabled");
                }
            });
    } else {
        $(".account_number").removeAttr("disabled");
    }
});

$("#bank_update").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);

    $.ajax({
        method: "post",
        url: "/updateBank/",
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

$("#genBank").on("submit", function (e) {
    e.preventDefault();
    const fd = $(this);

    $.ajax({
        method: "post",
        url: window.location.href,
        data: fd.serialize(),
        dataType: "json",
        processData: false,
        cache: false,
        beforeSend: function () {
            $(".genBank").attr("disabled", "disabled");
            $(".genBank").text("Generating...");
        },
        complete: function () {
            $(".genBank").removeAttr("disabled");
            $(".genBank").text("Generate");
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
        },
        error: function () {
            Swal.fire({
                type: "error",
                title: "Error!",
                html: "There was an error with the server. Please try later."
            })
        }
    });
});

$("select.network").on("change", function () {
    var name = $(this).children("option:selected").val();

    $(".amount").on("keyup", function () {
        var amount = Number($(".amount").val());
        if (name == "mtn") {
            mtp = $(".a2cmp").val();
            var net = Number($(".mtn-percentage").val());
            $(".send-amount").val('₦' + (Number(amount) * (mtp / 100)));
        } else if (name == "glo") {
            glp = $(".a2cgp").val();
            var net = Number($(".glo-percentage").val());
            $(".send-amount").val('₦' + (Number(amount) * (glp / 100)));
        } else if (name == "etisalat") {
            etp = $(".a2c9p").val();
            var net = Number($(".etisalat-percentage").val());
            $(".send-amount").val('₦' + (Number(amount) * (etp / 100)));
        } else if (name == "airtel") {
            aip = $(".a2cap").val();
            var net = Number($(".airtel-percentage").val());
            $(".send-amount").val('₦' + (Number(amount) * (aip / 100)));
        }
    });
});

$("#airtimeCash").on("submit", function (e) {
    e.preventDefault();


    var network = $(".network").val(); // get the selected network ID from the HTML input

    var mobile_number = $(".mobile_number").val();
    var amount = $(".amount").val();


    if (network == "" || amount == "" || mobile_number == "") {
        alert(" All fields are required");

    } else {
        var networkn = $(".network").find(":selected").val(); // get the selected country ID from the HTML input

        if (networkn == "mtn") {
            mtp = $(".a2cm").val();
            $("#opt1").text("How to Transfer on MTN")
            $("#opt2").text("Before you send an airtime, you Must have a 4 digit pin")
            $("#opt3").text("Press: *600 *000*Newpin*Newpin #")
            $("#opt4").text("Press: *600*"+mtp+ "*" + amount + "*PIN#")
            $("#amtm").text("₦" + amount)

            //$("#code").text(" How to transfer Airtime on MTN Share ’N’ Sell Dial: *600*081x6xxx8xx* " + amount +"*PIN#")
            //$("#instruct").text("Kindly Transfer the sum of  " + amount +" to 081x6xxx8xx ,follow the process below ")

        } else if (networkn == "glo") {
            glp = $(".a2cg").val();

            $("#opt1").text("How to Transfer on GLO")
            $("#opt2").text("Before you send an airtime, you Must have a 5 digit pin")

            $("#opt3").text("Press: *132 *00000*Newpin *Newpin #")
            $("#opt4").text("Press: *131*"+ glp +"*" + amount + "*PIN# ")
            $("#amtm").text("₦" + amount)

            //$("#code").text("How to transfer Airtime on GLO:  *131*080742991xx* " + amount +" *PIN# ")
            //$("#instruct").text("Kindly Transfer the sum of  " + amount +" to 080742991xx ,follow the process below ")

        } else if (networkn == "airtel") {
            aip = $(".a2ca").val();

            $("#opt1").text("How to Transfer on AIRTEL")
            $("#opt2").text("Before you send an airtime, you Must have a 4 digit pin")

            $("#opt3").html("Press: *432# " + "<br>" + " Select 'Pin Management' @ number4 option. " + "<br>" + " Press 1 to change pin." + "<br>" + "Your current Pin should be your default pin -- 0000 " + "<br>" + "Then Enter any NewPin.")
            $("#opt4").html(" Press: *432*1" + "*" +aip+ "" + "" + amount + "#")
            $("#amtm").text("₦" + amount)


        } else {
            etp = $(".a2c9").val();


            $("#opt1").text("How to Transfer on 9MOBILE")
            $("#opt2").text("Before you send an airtime, you Must have a 4 digit pin")

            $("#opt3").text("Press *247*0000*newpin#")
            $("#opt4").text("Press: *247*PIN*" + amount + ""+etp+"#")
            $("#amtm").text("₦" + amount)


        }
        $('#processModal').modal()
    }
});

function SubmitAirtime() {

    var network = $(".network").find(":selected").val(); // get the selected country ID from the HTML input
    var mobile_number = $(".mobile_number").val();
    var amount = $(".amount").val();
    var send_to = $(".fund").find(":selected").val();
    var amount_send = $(".send-amount").val();
    var token = $("#csrf").val();

    var networkn = $(".network option:selected").text(); // get the selected country ID from the HTML input

    if (networkn == "MTN") {
        mtn = $(".a2cm").val();
        var r = confirm("Are you sure you have sent " + " " + networkn + " " + "₦" + amount + " " + "to" + " " +mtn+ " to avoid your account and email been ban");

    } else if (networkn == "GLO") {
        gln = $(".a2cg").val();
        var r = confirm("Are you sure you have sent " + " " + networkn + " " + "₦" + amount + " " + "to" + " " +gln+ " to avoid your account and email been ban");

    } else if (networkn == "Airtel") {
        ain = $(".a2ca").val();
        var r = confirm("Are you sure you have sent " + " " + networkn + " " + "₦" + amount + " " + "to" + " " +ain+ " to avoid your account and email been ban");

    } else {
        etn = $(".a2c9").val();
        var r = confirm("Are you sure you have sent " + " " + networkn + " " + "₦" + amount + " " + "to" + " " +etn+ " to avoid your account and email been ban");

    }


    if (r == true) {
        $.ajax({
            method: 'POST',
            url: window.location.href,
            dataType: 'json',
            contentType: false,
            processData: false,
            cache: false,
            data: JSON.stringify({
                network: networkn,
                mobile: mobile_number,
                amount: amount,
                send_to: send_to,
                csrfmiddlewaretoken: token
            }),
            headers: { "X-CSRFToken": token },
            beforeSend: function () {
                $('#process2').css("display", "block");
                $('#subm').css("display", "none");

            },
            success: function (data) {
                if (data.status==true){
                    $('#ref').text(data.message);
                    $('#processModal').modal('hide');
                    $('#successModal').modal()
                } else{
                $('#errmessage').text(data.message);
                $('#processModal').modal('hide');
                $('#myModal').modal();
                }

            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                var parsed_data = JSON.parse(XMLHttpRequest.responseText);
                $('#errmessage').text(String(parsed_data.error));
                $('#processModal').modal('hide');
                $('#myModal').modal();



            },

            complete: function () {
                $('#process2').css("display", "none");
                $('#subm').css("display", "block");

            }
        });
    }
}

$("#bonus").on("submit", function (e) {
    e.preventDefault();
    const user_pin = $(".user_inp").val();
    const fd = $(this);

    Swal.fire({
        title: "Enter Transaction Pin",
        input: "password",
        showCancelButton: !0,
        confirmButtonText: "Submit",
        showLoaderOnConfirm: !0,
        confirmButtonColor: "#556ee6",
        cancelButtonColor: "#f46a6a",
        preConfirm: function (n) {
            return new Promise(function (t, e) {
                if (user_pin !== n) {
                    Swal.fire({
                        type: "error",
                        title: "Error!",
                        html: "Incorrect Transaction Pin"
                    })
                } else {
                    $.ajax({
                        type: "post",
                        url: window.location.href,
                        data: fd.serialize(),
                        dataType: "json",
                        success: function (res) {
                            if (res.status == true) {
                                Swal.fire({
                                    type: "success",
                                    title: "Successful",
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
                }
            })
        },
        allowOutsideClick: !1
    })
});



$("#id_network").change(function() {
    var networkId = $(this).val();
    $.ajax({ // initialize an AJAX request
        url: window.location.href,
        data: {
            'network': networkId
        },
        success: function(data) { 
            $("#id_network_amount").html(data);
        }
    });
});

$("#id_network_amount").change(function() {

    var selectednetwork = $("#id_network_amount option:selected").attr("amounttopay");
    var quantity = $("#id_quantity").val();
    amount_to_pay = "₦" + selectednetwork * quantity
$("#amount").text(amount_to_pay);
});

$("#id_quantity").keyup(function() {
    //var selectednetwork = $(this).children("option:selected").val();
    var selectednetwork = $("#id_network_amount option:selected").attr("amounttopay");
    var quantity = $("#id_quantity").val();
    amount_to_pay = "₦" + selectednetwork * quantity

    console.log(quantity)
    console.log(amount_to_pay)
    console.log(selectednetwork)

if (quantity > 39) {
        $("#amount").text("Maximum at a time is 39");

    }

else if (quantity < 1) {
        $("#amount").text("Minimum at a time is 39");

    }
else{

$("#amount").text(amount_to_pay);
}

});

 $("#rechargebtn").click(function() {
     const name = $("user_name").val();
        var network = $("#id_network").val(); // get the selected country ID from the HTML input
        var network_amount  = $("#id_network_amount").val();
        var name_on_card  = $("#id_name_on_card").val();
        var quantity  = $("#id_quantity").val();
        var token = $("csrf").val();
        var net = $("#id_network option:selected").text();

        Swal({
            title: "Dear "+name+",",
            text: "Are you sure you want to Generate " + " " + quantity + "  " + net + "  Recharge Pin"  ,
            icon: "warning",
            buttons:["Oh no!", "Yes"],
            dangerMode: true,
        })  .then((willDelete) => {
                if (willDelete) {
                     $.ajax({
                        type:'POST',
                        dataType: 'json',
                        contentType: "application/json",
                        beforeSend: function(){
                            //$('#process').css("display", "block");
                            //$('#btnsubmit').css("display", "none");
                            $.LoadingOverlay('show');
                                }, // initialize an AJAX request
                                url: url,
                                headers: { "X-CSRFToken": token },
                                data: JSON.stringify( {
                                    "network": network,
                                    "network_amount":network_amount,
                                    "quantity": quantity,
                                    "name_on_card":name_on_card
                                }),
                            success: function (data) {
                                $('#ref').text(String(data.id));
                                $('#net').text(String(data.network_name));
                                $('#amt').text(String(data.amount));
                                $('#q').text(String(data.quantity));
                                $('#status').text(String(data.Status));
                                $('#before').text(String(data.previous_balance));
                                $('#after').text(String(data.after_balance));
                                $('#mylink').attr("href",  "/Recharge-Pin-order/"+String(data.id));

                                swal({
                                    title: "Transaction Successful!",
                                    //text: "you successfully recharged",
                                    icon: "success",
                                    button: "View Pin!",
                                });
                                //
                                $('.swal-button--confirm').click(function(){
                                    $.ajax({
                                        beforeSend: function(){
                                            $.LoadingOverlay('show');
                                        },
                                        complete: function(){
                                            $.LoadingOverlay('hide');
                                        }
                                    })
                                    window.location.href = '/Recharge-Pin-order/' + String(data.id)
                                });

                                },
                            error: function(XMLHttpRequest, textStatus, errorThrown) {
                                $.LoadingOverlay('hide');
                                var parsed_data = JSON.parse(XMLHttpRequest.responseText);
                                $('#errmessage').text(String(parsed_data.error))
                                swal("Oops!",String(parsed_data.error), "error");
                                //   $('#myModal').modal()
                                },
                            complete: function(){
                                //$('#process').css("display", "none");
                                //$('#btnsubmit').css("display", "block");
                                $.LoadingOverlay('hide');
                                }
                            });
                //second ajax function ends
                }
                else {
                    swal("You pressed Cancel!");
                }
        });


   });


   $(".change_plan").on("submit", function (e) {
    e.preventDefault();
    const user_pin = $(".user_inp").val();
    const fd = $(this);

    Swal.fire({
        title: "Enter Transaction Pin",
        input: "password",
        showCancelButton: !0,
        confirmButtonText: "Submit",
        showLoaderOnConfirm: !0,
        confirmButtonColor: "#556ee6",
        cancelButtonColor: "#f46a6a",
        preConfirm: function (n) {
            return new Promise(function (t, e) {
                if (user_pin !== n) {
                    Swal.fire({
                        type: "error",
                        title: "Error!",
                        html: "Incorrect Transaction Pin"
                    })
                } else {
                    $.ajax({
                        type: "post",
                        url: window.location.href,
                        data: fd.serialize(),
                        dataType: "json",
                        success: function (res) {
                            if (res.status == true) {
                                Swal.fire({
                                    type: "success",
                                    title: "Successful",
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
                }
            })
        },
        allowOutsideClick: !1
    })
});

// $("#btnSubmit").on("submit", function (e) {
//     e.preventDefault();
//     alert("Cool")
//     var url = "/airtime_funding/"; // get the url of the `load_cities` view
//     var network = $(".network").find(":selected").val(); // get the selected country ID from the HTML input
//     var mobile_number = $(".mobile_number").val();
//     var amount = $(".amount").val();
//     var amount_send = $(".send-amount").val();
//     var token = $(".csrf").val();;

//     var networkn = $("#.network option:selected").text(); // get the selected country ID from the HTML input

//     if (networkn == "MTN") {
//         var r = confirm("Are you sure you have sent " + " " + networkn + " " + "N" + amount + " " + "to" + " " + "081x6xxx8xx to avoid your account and email been ban");

//     } else if (networkn == "GLO") {
//         var r = confirm("Are you sure you have sent " + " " + networkn + " " + "N" + amount + " " + "to" + " " + "080742991xx to avoid your account and email been ban");

//     } else if (networkn == "Airtel") {
//         var r = confirm("Are you sure you have sent " + " " + networkn + " " + "N" + amount + " " + "to" + " " + "091244050xx to avoid your account and email been ban");

//     } else {
//         var r = confirm("Are you sure you have sent " + " " + networkn + " " + "N" + amount + " " + "to" + " " + "090949092xx to avoid your account and email been ban");

//     }


//     if (r == true) {
//         $.ajax({
//             type: 'POST',
//             dataType: 'json',
//             contentType: "application/json",
//             beforeSend: function () {
//                 $('#process2').css("display", "block");
//                 $('#subm').css("display", "none");

//             }, // initialize an AJAX request
//             url: url,
//             headers: {
//                 "X-CSRFToken": token
//             },
//             data: JSON.stringify({
//                 "network": network,
//                 "mobile_number": mobile_number,
//                 "amount": amount
//             }),
//             success: function (data) {

//                 console.log(data);
//                 console.log(data.id);
//                 $('#ref').text(String(data.ident));
//                 $('#processModal').modal('hide');
//                 $('#successModal').modal()

//             },
//             error: function (XMLHttpRequest, textStatus, errorThrown) {
//                 var parsed_data = JSON.parse(XMLHttpRequest.responseText);
//                 $('#errmessage').text(String(parsed_data.error));
//                 $('#processModal').modal('hide');
//                 $('#myModal').modal();



//             },

//             complete: function () {
//                 $('#process2').css("display", "none");
//                 $('#subm').css("display", "block");

//             }
//         });
//     }
// });