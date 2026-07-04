async function checkAnswer(btn) {
    wordButtons = document.querySelectorAll(".btns button");

    const hasEnabledButton = [...wordButtons].some(btn => !btn.disabled);

    if (hasEnabledButton) {
        return;
    }


    const url = btn.dataset.url
    const id = btn.dataset.id


    let my_ans = []

    for (const element of answerButtons) {
        my_ans.push(element.innerText.trim().toLowerCase())
    }

    const userAnswer = my_ans.join(" ");


    let res = await getNextGame(id, userAnswer, url, btn)
    if (res) {
        confetti({
            angle: randomInRange(55, 125),
            spread: randomInRange(50, 70),
            particleCount: randomInRange(50, 100),
            origin: { y: .6 }
        });

        if (res.xp) {
            let xplcxp = document.querySelector("#xplcxp > span")
            let xplcl = document.querySelector("#xplcl > span")
            xplcxp.innerHTML = res.xp
            xplcl.innerHTML = res.level
        }

    }

} 