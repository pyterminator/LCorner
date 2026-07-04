async function nextGame(btn){
    let ans = btn.dataset.ans.trim()
    const url = btn.dataset.url 
    const id = btn.dataset.id


    await getNextGame(id, ans, url, btn)
}