async function postLike(i){
    const url = i.dataset.url
    const id = i.dataset.id

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
        i.className = "fa-solid fa-heart"
        i.nextElementSibling.innerText = data.new_like_count
    }
}