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
    if (!my_select.classList.contains('disabled')) {
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

function openPriceSelect(inp) {
    const price = inp.parentElement.parentElement.nextElementSibling
    if (inp.getAttribute('value') == 1) {
        price.classList.remove("disabled")
    } else if (inp.getAttribute('value') == 0) {
        price.classList.add("disabled")
    }
}


function showPassword(i) {
    const password_input = i.parentElement.nextElementSibling
    if (password_input.getAttribute("type") == "password") {
        password_input.type = "text"
        password_input.placeholder = "Ş i f r ə n i z"
        i.className = "fa-solid fa-eye-slash"
    } else {
        password_input.type = "password"
        password_input.placeholder = "* * * * * * * *"
        i.className = "fa-solid fa-eye"
    }
}


function validateUsername(inp) {
    const alert_box = inp.nextElementSibling
    const username = inp.value

    if (username == "") {
        alert_box.innerText = "İstifadəçi adı boş ola bilməz!"
    } else if (username.length <= 2) {
        alert_box.innerText = "İstifadəçi adı minimum 3 simvoldan ibarət olmalıdır!"
    } else if (!/^[a-z]+$/.test(username)) {
        alert_box.innerText = "İstifadəçi adında yalnız ingiliscə kiçik hərflər ola bilər!"
    } else {
        alert_box.innerText = ""
    }
}

function validatePassword(inp) {
    const alert_box = inp.nextElementSibling
    const password = inp.value
    const repassword = inp.parentElement.querySelector("input[name=repassword]")

    if (password == "") {
        alert_box.innerText = "Şifrənizi daxil edin!"
    } else if (password.length <= 7) {
        alert_box.innerText = "Şifrə minimum 8 simvoldan ibarət olmalıdır"
    } else if (!/[A-Z]/.test(password)) {
        alert_box.innerText = "Şifrədə böyük hərf də olmalıdır!";
    } else if (!/[a-z]/.test(password)) {
        alert_box.innerText = "Şifrədə kiçik hərf də olmalıdır!";
    } else if (!/[0-9]/.test(password)) {
        alert_box.innerText = "Şifrədə rəqəm də olmalıdır!";
    } else {
        alert_box.innerText = ""
    }


    validateRePassword(repassword)
}


function validateEmail(inp) {
    const alert_box = inp.nextElementSibling
    const EMAIL_PATTERN = /^[A-Za-z0-9](?:[A-Za-z0-9._-]{1,}[A-Za-z0-9])?@[A-Za-z0-9](?:[A-Za-z0-9-]{0,}[A-Za-z0-9])?(?:\.[A-Za-z]{2,})+$/;
    if (!EMAIL_PATTERN.test(inp.value)) {
        alert_box.innerText = "E-mail doğru formatda deyil!"
    } else {
        alert_box.innerText = ""
    }
}


function validateRePassword(inp) {
    const password = inp.parentElement.querySelector("input[name=password]").value
    const repassword = inp.value
    const alert_box = inp.nextElementSibling



    if (password != repassword) {
        alert_box.innerText = "Şifrələr eyni deyil!"
    } else {
        alert_box.innerText = ""
    }
}


function ToggleSidebarMenu(span) {
    const sidebar = document.querySelector("#root > div:nth-child(1)")
    const blank = document.querySelector("#root > div:nth-child(2)")



    if (span.dataset.val == "1") {
        sidebar.style.display = "none"
        sidebar.style.left = "0"
        blank.style.width = "100%";
        blank.style.marginLeft = "0";
        span.dataset.val = "0"
    } else {
        sidebar.style.display = "block"
        sidebar.style.left = "0"
        blank.style.width = "calc(100% - 25rem)";
        blank.style.marginLeft = "25rem";
        span.dataset.val = "1"
    }
}

function closeModal(btn) {
    btn.parentElement.parentElement.parentElement.style.display = "none"
}

function deleteAndCloseModal(btn) {
    const delete_url = btn.closest(".main-modal").dataset.url
    window.location.href = delete_url
}

function openModal(event) {
    event.preventDefault()

    const modal = event.currentTarget
        .closest(".table")
        .querySelector(".main-modal")

    modal.style.display = "flex"
    modal.dataset.url = event.currentTarget.getAttribute("href")
}

function MobileToggleSidebarMenu(btn) {
    const sidebar = document.querySelector("#root > div:nth-child(1)")
    const blank = document.querySelector("#root > div:nth-child(2)")

    sidebar.style.display = "block";
    sidebar.style.left = "0";
    sidebar.querySelector(".carpet").style.right = "0"
}

function CloseMobileSidebar(btn) {
    btn.parentElement.parentElement.style.left = "-25rem"
    btn.parentElement.parentElement.querySelector(".carpet").style.right = "-200%"
}


function removeAlert(span) {
    span.parentElement.remove()
}

// Bütün şəkillərin sağ kliklenmesini kilidle
const all_images = document.querySelectorAll("img")
all_images.forEach(element => {
    element.addEventListener("contextmenu", function (event) {
        event.preventDefault();
        return false;
    })
});

// CSRF generate et
window.getCookie = function(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;
            }
        }
    }
    return cookieValue;
};

// Bildirisleri yoxla
async function GetUnreadNotificationCount(){
    const baseUrl = window.location.origin
    const url = baseUrl + "/notifications/get-unread-notification-count/"

    const response = await fetch(url, {
        method: "POST",

        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })

    const data = await response.json()
    if (data.success && data.has_unread_notifications){
        document.getElementById("has_notify").style.display = "inline-block"
    } else {
        document.getElementById("has_notify").style.display = "none"
    }
}


let interval = setInterval(GetUnreadNotificationCount, 10000);
document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
        clearInterval(interval);
    } else {
        interval = setInterval(GetUnreadNotificationCount, 10000);
    }
});


function copyLinkWithRC(btn){
    const url = btn.dataset.url;
    const ref = btn.dataset.ref;

    const fullUrl = new URL(url, window.location.origin);
    fullUrl.searchParams.set("ref", ref);

    navigator.clipboard.writeText(fullUrl.toString());

    btn.innerHTML = '<i class="fa-solid fa-check"></i> Kopyalandı';
    
    setTimeout(() => {
        btn.innerHTML = '<i class="fa-regular fa-copy"></i> Linki kopyala';
    }, 3000);
}