async function checkAsRead(div){
    const url = div.dataset.url 
    const id = div.dataset.id 

    const response = await fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            "id": id
        })
    });

    const data = await response.json();

    if(data.success){
        div.classList = "check_as_read checked_as_read"
        div.querySelector("span").innerText = "Oxundu kimi işarələndi"
        div.querySelector("i").classList = "fa-solid fa-check-double"
    }
}