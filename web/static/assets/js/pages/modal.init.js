var exampleModal = document.getElementById("exampleModal");
exampleModal.addEventListener("show.bs.modal", function (e) {
    var t = e.relatedTarget.getAttribute("data-bs-whatever"),
        a = exampleModal.querySelector(".modal-title"),
        e = exampleModal.querySelector(".modal-body input");
    a.textContent = "New message to " + t, e.value = t
});