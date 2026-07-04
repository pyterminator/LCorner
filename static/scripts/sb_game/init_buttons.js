function initButtons() {
        

    wordButtons = document.querySelectorAll(".btns button");
    answerButtons = document.querySelectorAll(".box button");
    let index = 0;


    wordButtons.forEach(btn => {
        btn.addEventListener("click", function () {

            if (index >= answerButtons.length) return;

            answerButtons[index].textContent = this.textContent;
            answerButtons[index].removeAttribute("disabled")
            index++;

            // Eyni sözü iki dəfə seçməmək üçün
            this.disabled = true;
        });
    });

    answerButtons.forEach(btn => {
        btn.addEventListener("click", function () {


            if (this.textContent === "") return;

            wordButtons.forEach(element => {
                if(element.textContent === this.textContent){
                    element.removeAttribute("disabled")
                }
            });

            this.textContent = "";
            this.setAttribute("disabled", true);
            box.appendChild(this);
            answerButtons = document.querySelectorAll(".box button");
            

            index--;
        });
    });
}

initButtons();