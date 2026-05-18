
async function changePostApproved(div){
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

function getCookie(name) {

    let cookieValue = null

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";")

        for (let cookie of cookies) {

            cookie = cookie.trim()

            if (cookie.startsWith(name + "=")) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                )

                break
            }
        }
    }

    return cookieValue
}