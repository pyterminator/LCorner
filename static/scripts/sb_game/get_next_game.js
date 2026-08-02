async function getNextGame(id, userAnswer, url, btn) {
    const response = await fetch(url, {
        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },

        body: JSON.stringify({
            "id": id,
            "user_answer": userAnswer
        })
    })

    const data = await response.json()

    if (data.success) {


        let btns = document.querySelector(".btns")
        box.innerHTML = ""
        btns.innerHTML = ""
        for (const w of data.words) {
            btns.innerHTML += `<button>${w}</button>`
            box.innerHTML += "<button disabled></button>"
        }

        initButtons();

        document.querySelector(".sentence-builder .check button").dataset.id = data.id
        document.querySelector(".sentence-builder .links #next").dataset.id = data.id
        document.querySelector(".sentence-builder .links #next").dataset.ans = data.answer
        document.querySelector(".game-title p.sb-alert").innerText = ""

        let modal_p = document.querySelector(".sentence-builder .modal p")
        modal_p.innerHTML = `${data.answer}<span class="hr"></span>${data.description}`
        return {
            "xp": data.xp,
            "level": data.level
        }
    } else {
        document.querySelector(".game-title p.sb-alert").innerText = data.message
        answerButtons.forEach(element => {
            element.click()
        });
        return false
    }
}