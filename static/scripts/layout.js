// Ctrl+ zoom block
document.addEventListener("keydown", function(e){

    if (
        e.ctrlKey &&
        (
            e.key === "+" ||
            e.key === "-" ||
            e.key === "="
        )
    ){
        e.preventDefault()
    }

});

// Mouse zoom block
document.addEventListener("wheel", function(e){

    if (e.ctrlKey){
        e.preventDefault()
    }

}, { passive:false });

// Change Themes
function toggleThemeSwitch(el) {
    const html = document.documentElement;

    const current = html.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";

    html.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);

    el.classList.toggle("switchery-on");
}

// Load theme
window.addEventListener("load", () => {
    const saved = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", saved);

    const switchery = document.querySelector(".menu .switchery");

    if (switchery) {
        if (saved === "light") {
            switchery.classList.add("switchery-on");
        } else {
            switchery.classList.remove("switchery-on");
        }
    }
});

// Load layout
window.addEventListener("load", function () {
    setTimeout(() => {
        document.querySelector(".layout-loader").style.display = "none";
        document.body.removeAttribute("style")
    }, 100);
});

// Bütün şəkillərin sağ kliklenmesini kilidle
const all_images = document.querySelectorAll("img")
all_images.forEach(element => {
    element.addEventListener("contextmenu", function (event) {
        event.preventDefault();
        return false;
    })
});