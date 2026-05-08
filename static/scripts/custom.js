function openDropdownMenu(btn) {
    const menu = btn.nextElementSibling
    if (getComputedStyle(menu).display == "none") {
        menu.style.display = "flex"
    } else {
        menu.style.display = "none"
    }
}


function openSelect(header) {
    const my_select = header.closest(".select")
    if (!my_select.classList.contains('disabled')){
        my_select.classList.toggle("opened")
    }
}

function setValueSelect(option) {
    const select_input = option.parentElement.previousElementSibling.previousElementSibling
    select_input.setAttribute("value", option.getAttribute("data-val"))
    showSelectValue(select_input)
}


function showSelectValue(inp) { 
    const select_span = inp.parentElement.querySelector(".header p span")
    select_span.innerText = inp.value
    openSelect(inp.parentElement.querySelector(".header"))
}

function openPriceSelect(inp){
    const price = inp.parentElement.parentElement.nextElementSibling
    if (inp.getAttribute('value')==1){
        price.classList.remove("disabled")
    } else if (inp.getAttribute('value')==0) {
        price.classList.add("disabled")
    }
}