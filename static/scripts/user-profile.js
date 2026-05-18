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
