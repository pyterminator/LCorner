async function changeUserProfile(input){

    const avatar_loader = input.closest(".img-container").querySelector(".loader")
    avatar_loader.style.display = "flex"

    const file = input.files[0]
    const url = input.closest(".change-profile-photo").dataset.action


    if (!file) return;

    const formData = new FormData();
    formData.append("avatar", file); 

    const response = await fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": input.previousElementSibling.value
        },
        body: formData
    });

    const data = await response.json();
    setTimeout(() => {
        if(data.success){
            changeUserProfileUI(input.closest(".img-container").querySelector(":scope > img"), file)
            document.getElementById("avatar-errors").innerText = ""
    
        } else {
            document.getElementById("avatar-errors").innerText = data.error
        }
        avatar_loader.style.display = "none";
    }, 2000);
}

function changeUserProfileUI(img_element, file){
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function (event) {
        img_element.src = event.target.result;
        if(img_element.getAttribute("id")){
            img_element.removeAttribute("id") 
        }
    };
}


function editBaData(button){
    button.nextElementSibling.style.display = "block";
    let fullname = button.parentElement.parentElement.querySelector(".fullname")
    let username = button.parentElement.parentElement.querySelector(".username")
    let profession = button.parentElement.parentElement.querySelector(".profession")

    fullname.style.display = "none"
    username.style.display = "none"
    profession.style.display = "none"

    button.style.display = "none";
}

function closeEditBaData(button){ 
    const f = button.parentElement.parentElement
    const par = f.parentElement.parentElement
    par.querySelector(".fullname").style.display = "flex"
    par.querySelector(".username").style.display = "block"
    par.querySelector(".profession").style.display = "block"
    f.style.display = "none"
    f.reset()
    f.previousElementSibling.style.display = "block"
}

async function updateBaseData(e){
    e.preventDefault()
    let f = e.target
    let url = f.getAttribute("action")

    f.querySelectorAll(".form-input-alert").forEach(ale => {
        ale.innerText = ""
    });

    const f_n = f.first_name.value
    const l_n = f.last_name.value
    const p_ = f.profession.value

    const formData = new FormData(); 

    const response = await fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": f.csrfmiddlewaretoken.value
        },
        body: JSON.stringify({
            "first_name": f_n,
            "last_name":l_n,
            "profession":p_
        })
    });

    const data = await response.json();

    if(data.success){
        closeEditBaData(f.querySelector("#ignore-ba-data"))
        document.querySelector("div.fullname > .first-name").innerText = data.data.first_name
        f.first_name.value = data.data.first_name
        document.querySelector("div.fullname > .last-name").innerText = data.data.last_name
        f.last_name.value = data.data.last_name
        document.querySelector("div.col > .profession").innerText = data.data.profession
        f.profession.value = data.data.profession
        // f.previousElementSibling.style.display = "none"
    } else if (data.f_n) {
        f.querySelector("#form_data_first_name + p").innerText = data.f_n
    } else if (data.l_n) {
        f.querySelector("#form_data_last_name + p").innerText = data.l_n
    } else if (data.p_) {
        f.querySelector("#form_data_profession + p").innerText = data.p_
    } else {
        f.querySelector("#form_data_profession + p").innerText = data.error
    }
}

function editBioData(btn){
    const bio_content = btn.parentElement.previousElementSibling;

    bio_content.setAttribute('contenteditable', true);
    setCursorToEnd(bio_content);

    btn.nextElementSibling.style.display = "flex";
    btn.style.display = "none";
}

function setCursorToEnd(el) {
    el.focus();

    const range = document.createRange();
    const selection = window.getSelection();

    range.selectNodeContents(el);
    range.collapse(false); // false = sonuna aparır

    selection.removeAllRanges();
    selection.addRange(range);
}


function closeEditBioData(btn){
    btn.parentElement.parentElement.previousElementSibling.setAttribute("contenteditable", false);
    btn.parentElement.previousElementSibling.style.display = "inline-block";
    
    const txt = document.querySelector(".hidden-bio-text").innerText;
    btn.parentElement.parentElement.previousElementSibling.innerText = txt;
    btn.parentElement.style.display = "none";
    const alert_box = btn.closest(".col").querySelector(".bio-alert");
    alert_box.innerText = ""
    alert_box.style.display = "none"; 
}

async function saveBioData(btn){
    let bio_content = btn.closest(".col").querySelector(".bio-content")
    let alert_box = bio_content.previousElementSibling.previousElementSibling
    
    const url = btn.dataset.url

    const response = await fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            "bio": bio_content.innerText
        })
    });

    const data = await response.json();

    if (data.success){
        bio_content.previousElementSibling.innerText = data.bio 
        closeEditBioData(btn.nextElementSibling)
    } else {
        alert_box.style.display = "block"
        alert_box.innerText = data.error
    }

}