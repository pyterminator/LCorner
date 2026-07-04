// Bildirisleri ve layout xp|level -i yoxla
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
    
    if (data.success){
        let xplcxp = document.querySelector("#xplcxp > span")
        let xplcl = document.querySelector("#xplcl > span")
        xplcxp.innerHTML = data.xp 
        xplcl.innerHTML = data.level

    }

    if (data.success && data.has_unread_notifications){
        document.getElementById("has_notify").style.display = "inline-block"
    } else {
        document.getElementById("has_notify").style.display = "none"
    }
}
// Sayt açıldıqda bir dəfə işlət
GetUnreadNotificationCount()