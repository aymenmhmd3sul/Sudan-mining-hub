document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll("button").forEach(btn => {
        btn.addEventListener("click", function () {
            alert(this.innerText);
        });
    });

});
