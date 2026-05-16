

async function switcheryToggle(div){
    if (div.getAttribute("data-type") == "changeMessageRead"){
        const changed = await changeMessageRead(div)
        if (changed){
            div.classList.toggle("switchery-on")
        }
    } else if (div.dataset.type == "changeMessagePublic"){
        const changed = await changeMessagePublic(div)
        if (changed){
            div.classList.toggle("switchery-on")
        }
    }
}