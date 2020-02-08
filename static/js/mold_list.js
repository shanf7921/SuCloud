$(document).ready(function () {
    adduser = document.getElementById('add-mold-btn')
    adduserquit = document.getElementById('add-mold-quit')
    addacount = document.getElementById('add-mold-div')

    adduser.addEventListener("click", function () {
        addacount.style.display = "block"
    }, false)

    adduserquit.addEventListener("click", function () {
        addacount.style.display = "none"
    }, false)

     /*addsubmit = document.getElementById('add-mold-submit')
    addsubmit.addEventListener("click", function () {
        document.form.value.clear();
    })*/


})