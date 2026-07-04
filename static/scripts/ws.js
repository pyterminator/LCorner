const socket = new WebSocket("ws://" + window.location.host + "/ws/notifications/");

socket.onmessage = (event) => { 
    const data = JSON.parse(event.data); 

    let xplcxp = document.querySelector("#xplcxp > span")
    let xplcl = document.querySelector("#xplcl > span")
    xplcxp.innerHTML = data.xp 
    xplcl.innerHTML = data.level

    if (data.notification_count > 0){
        document.getElementById("has_notify").style.display = "inline-block"
    } else {
        document.getElementById("has_notify").style.display = "none"
    }
}
  