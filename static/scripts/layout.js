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

// Message Box
 function CreateMessageBox(message_type, message_text){
    let div_1 = document.createElement("div")
    div_1.className = `alert alert-${message_type}`

    if (message_type=="error"){
        let i_1 = document.createElement("i")
        i_1.className = "fa-solid fa-triangle-exclamation" 
        div_1.appendChild(i_1)
    } else if (message_type == "success"){
        let i_1 = document.createElement("i")
        i_1.className = "fa-regular fa-circle-check" 
        div_1.appendChild(i_1) 
    }

    let p_1 = document.createElement("p")
    p_1.innerText = message_text
    div_1.appendChild(p_1)

    let span_1 = document.createElement("span")
    span_1.className = "fa-solid fa-xmark"
    span_1.setAttribute("onclick", "this.parentElement.remove()") 
    div_1.appendChild(span_1)

    return div_1
}
