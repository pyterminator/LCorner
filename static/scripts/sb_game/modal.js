// Modal
function openSentenceBuilderModal(btn){
    let modal = document.querySelector(".sentence-builder .modal")

    if(btn.dataset.val == "off"){
        btn.dataset.val = "on"
        modal.style.display = "flex"
        modal.classList.add("animate__backInDown")
    } else {
        btn.dataset.val = "off"
        modal.classList.remove("animate__backInDown")
        modal.classList.add("animate__backOutDown")
        setTimeout(() => {
            modal.style.display = "none"
            modal.classList.remove("animate__backOutDown")
        }, 250);
    }
}

function closeSentenceBuilderModal(btn){
    let b = document.getElementById("open-close-sentence-builder-modal")
    b.click()
} 