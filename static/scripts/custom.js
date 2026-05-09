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


function showPassword(i){
    const password_input = i.parentElement.nextElementSibling
    if (password_input.getAttribute("type") == "password"){
        password_input.type = "text"
        password_input.placeholder = "Ş i f r ə n i z" 
        i.className = "fa-solid fa-eye-slash"
    } else {
        password_input.type = "password"
        password_input.placeholder = "* * * * * * * *"
        i.className = "fa-solid fa-eye"
    }
}


function validateUsername(inp){
    const alert_box = inp.nextElementSibling
    const username = inp.value 

    if(username == ""){
        alert_box.innerText = "İstifadəçi adı boş ola bilməz!"
    } else if (username.length <= 2){
        alert_box.innerText = "İstifadəçi adı minimum 3 simvoldan ibarət olmalıdır!"
    } else if (!/^[a-z]+$/.test(username)){
        alert_box.innerText = "İstifadəçi adında yalnız ingiliscə kiçik hərflər ola bilər!"
    } else {
        alert_box.innerText = ""
    }
}

function validatePassword(inp){
    const alert_box = inp.nextElementSibling
    const password = inp.value 
    const repassword = inp.parentElement.querySelector("input[name=repassword]")

    if(password == ""){
        alert_box.innerText = "Şifrənizi daxil edin!"
    } else if (password.length <= 7){
        alert_box.innerText = "Şifrə minimum 8 simvoldan ibarət olmalıdır"
    } else {
        alert_box.innerText = ""
    }

    
    validateRePassword(repassword)
}


function validateRePassword(inp){
    const password = inp.parentElement.querySelector("input[name=password]").value
    const repassword = inp.value 
    const alert_box = inp.nextElementSibling

 

    if (password != repassword){
        alert_box.innerText = "Şifrələr eyni deyil!"
    } else {
        alert_box.innerText = ""
    }
}