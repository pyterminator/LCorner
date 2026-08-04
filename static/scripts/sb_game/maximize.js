function toggleSBGame(btn) {
    if (document.fullscreenElement) {
        document.exitFullscreen();
        document.body.querySelector("#xp-level").style.backgroundColor = "transparent";
    } else {
        document.body.requestFullscreen();
        document.body.querySelector("#xp-level").style.backgroundColor = "var(--main)";
    }
}

document.addEventListener("fullscreenchange", () => {
    const btn = document.querySelector("#sb-game-maximize-btn");
    const icon = btn.querySelector("i");

    icon.className = document.fullscreenElement
        ? "fa-solid fa-times"
        : "fa-solid fa-maximize";
});