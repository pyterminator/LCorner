async function changeMessageRead(div){
    const data_url = div.dataset.url

    const response = await fetch(data_url, {
        method: "POST",

        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })

    const data = await response.json()

    return data.success
}


async function changeMessagePublic(div){
    const data_url = div.dataset.url

    const response = await fetch(data_url, {
        method: "POST",

        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })

    const data = await response.json()

    return data.success
}
