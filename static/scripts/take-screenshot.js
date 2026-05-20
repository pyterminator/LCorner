async function takeScreenShot(btn){
    btn.style.display = "none"
    const konteyner = btn.closest(".post-detail")

    await document.fonts.ready

    const canvas = await html2canvas(konteyner, {
        scale: window.devicePixelRatio * 2,
        useCORS: true,
        backgroundColor: null
    })

    const image = canvas.toDataURL("image/png")

    const a = document.createElement("a")

    let fileName = btn.dataset.name.trim()

    fileName = fileName.replace(/[\\/:*?"<>|]/g, "")

    a.href = image
    a.download = fileName + ".png"

    a.click()
    btn.style.display = "inline-block"
}