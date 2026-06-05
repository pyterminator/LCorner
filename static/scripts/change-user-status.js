async function changeUserStaff(div){
    const data_url = div.dataset.url
    const data_id = div.dataset.id 
    var is_staff = true

    if (div.classList.contains("swithery-on")){
        is_staff = false        
    }

    const response = await fetch(data_url, {
        method: "POST",

        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(
            {"id": data_id, "is_staff": is_staff}
        )
    })

    const data = await response.json()

    return data.success
}