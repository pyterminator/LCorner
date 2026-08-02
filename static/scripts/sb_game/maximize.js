function toggleSBGame(btn) {
    if (document.fullscreenElement) {
        document.exitFullscreen();
    } else {
        document.body.requestFullscreen();
    }
}

document.addEventListener("fullscreenchange", () => {
    const btn = document.querySelector("#sb-game-maximize-btn");
    const icon = btn.querySelector("i");

    icon.className = document.fullscreenElement
        ? "fa-solid fa-times"
        : "fa-solid fa-maximize";
});