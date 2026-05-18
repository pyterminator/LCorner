function resizePost(dots){ 

    const short_desc = dots.closest(".post").querySelector(".short-desc")
    const long_desc = dots.closest(".post").querySelector(".long-desc")

    if (dots.dataset.val == "off"){


        dots.parentElement.parentElement.querySelectorAll(".post").forEach(element => {
            if (element.getAttribute("style")){
                element.removeAttribute("style")
                element.querySelector(".dots").dataset.val = "off"
                element.querySelector(".short-desc").removeAttribute("style")
                element.querySelector(".long-desc").removeAttribute("style")
            }
        });

        dots.dataset.val = "on"
        dots.parentElement.style.width = "100%"
        dots.parentElement.style.zoom = "1.5"
        dots.parentElement.style.margin = "1rem 0"

        short_desc.style.display = "none"
        long_desc.style.display = "block"
    } else {
        dots.dataset.val = "off"
        dots.parentElement.removeAttribute("style")

        short_desc.removeAttribute("style")
        long_desc.removeAttribute("style")
    }
}