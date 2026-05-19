async function changeUserProfile(input){
    const file = input.files[0]
    const url = input.parentElement.getAttribute("action")

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
    if(data.success){
        changeUserProfileUI(input.closest(".avatar").querySelector("img"), file)
    }

}


async function deleteUserProfile(div){
    const url = div.dataset.url  
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
    });
    const data = await response.json();
    if(data.success){ 
        const i = div.parentElement.querySelector("img")
        i.id = "default-avatar"
        i.src = div.parentElement.dataset.default

        div.previousElementSibling.style.display = "none"
        div.style.display = "none"
    }
}


function changeUserProfileUI(img_element, file){
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function (event) {
        img_element.src = event.target.result;
        if(img_element.getAttribute("id")){
            img_element.removeAttribute("id") 

            
            const delete_avatar = document.createElement("div")
            delete_avatar.setAttribute("onclick", "deleteUserProfile(this)")
            delete_avatar.innerHTML = `<i class="fa-solid fa-trash"></i>`
            delete_avatar.className = "delete-avatar"
            delete_avatar.setAttribute("data-url", "/delete-my-avatar" )

 
            img_element.insertAdjacentElement("afterend", delete_avatar);

            const expand = document.createElement("div")
            expand.setAttribute("onclick", "expandAvatar(this)")
            expand.innerHTML = `<i class="fa-solid fa-expand"></i>`
            expand.className = "expand"

            img_element.insertAdjacentElement("afterend", expand);
              

        }
    };
}


function expandAvatar(expand){
    const avatar_max = expand.parentElement.previousElementSibling
    const ami = avatar_max.querySelector("img")


    ami.src = document.querySelector(".avatar > img").src
    avatar_max.style.display = "flex";
}

function closeAvatar(cl){
    cl.parentElement.style.display = "none";
}

