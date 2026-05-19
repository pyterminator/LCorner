function validateName(inp) {
    const alert_box = inp.nextElementSibling;
    const username = inp.value.trim();

    const validName = /^[A-ZÇŞƏĞÖÜİ][a-zçşəğöüıi]+$/;

    if (username === "") {
        alert_box.innerText = "Ad boş ola bilməz!"; 
    } 
    else if (username.length < 3) {
        alert_box.innerText = "Ad minimum 3 simvoldan ibarət olmalıdır!";
    } 
    else if(username.length > 15){
        alert_box.innerText = "Ad maksimum 15 simvoldan ibarət ola bilər!"
    }
    else if (!validName.test(username)) {
        alert_box.innerText = "Adın yalnız birinci hərfi böyük, qalanları isə kiçik hərf olmalıdır!";
    } 
    else {
        alert_box.innerText = "";
        return true 
    }

    return false
}

function validateEmail(inp){
    const alert_box = inp.nextElementSibling
    const EMAIL_PATTERN = /^[A-Za-z0-9](?:[A-Za-z0-9._-]{1,}[A-Za-z0-9])?@[A-Za-z0-9](?:[A-Za-z0-9-]{0,}[A-Za-z0-9])?(?:\.[A-Za-z]{2,})+$/;
    if(!EMAIL_PATTERN.test(inp.value)){
        alert_box.innerText = "E-mail doğru formatda deyil!"
    } else if(inp.value.length > 50){
        alert_box.innerText = "E-mail maksimum 50 simvoldan ibarət ola bilər!"
    } else {
        alert_box.innerText = ""
        return true
    }

    return false
}


function validateMessage(textarea) {
    const alert_box = textarea.nextElementSibling;
    const message = textarea.value.trim();

    const validMessage = /^[A-Za-zÇŞƏĞÖÜİçşəğöüıi0-9\s.!,?]+$/;

    if (message === "") {
        alert_box.innerText = "Mesaj boş ola bilməz!";
    } 
    else if (message.length < 5) {
        alert_box.innerText = "Mesaj minimum 5 simvol olmalıdır!";
    } 
    else if (message.length > 255) {
        alert_box.innerText = "Mesaj maksimum 255 simvol ola bilər!";
    } 
    else if (!validMessage.test(message)) {
        alert_box.innerText = "Yalnız hərf, rəqəm, boşluq və . ! ? istifadə edə bilərsiniz!";
    } 
    else {
        alert_box.innerText = "";
        return true
    }
    return false
}


function validateContactForm(){
    const name = document.getElementById("name_field");
    const email = document.getElementById("email_field");
    const message = document.getElementById("message_field");

    const validName = validateName(name);
    const validEmail = validateEmail(email);
    const validMessage = validateMessage(message);

    if (validName && validEmail && validMessage) {
        return true;
    } else {
        return false;
    }
}