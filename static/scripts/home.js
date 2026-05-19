async function postLike(div){
    const url = div.dataset.url
    const id = div.dataset.id

    const response = await fetch(url, {
        method:"POST",
        headers:{
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: id
        })
    });

    const data = await response.json()

    if (data.liked){
        div.querySelector("span.like > b").innerText = data.new_like_count
    }
}