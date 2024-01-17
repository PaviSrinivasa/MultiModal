
async function getName() {
    $('.js-popup-link').click(function(e){
    e.preventDefault()
    $.ajax({
        url: 'popup',
        success: function(context) {
            const data = response.context
            console.log(data)
            let dataResponse = await response.json()
            let ul = document.getElementById('fol')
            let li = document.createElement('li')
            li.innerHTML = await dataResponse['context']
            ul.appendChild(li)
        }
    });

    /*
    $("#dialog-form").html(context).dialog({modal:true}).dialog('open');
    $("#dialog-form").dialog({modal: true}).dialog('open').load("popup.html")
    $("#dialog-form").html(data).dialog({modal:true}).dialog('open'); */
   })
    /* let response = await fetch('/',{
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json'
            }
    })
    let data = await response.json()
    let ul = document.getElementById('fol')
    let li = document.createElement('li')
    li.innerHTML = await data['context']
    ul.appendChild(li) */
}

/* // Get the elements by their ID
var popupLink = document.getElementById("customFile");
var popupWindow = document.getElementById("popup-window");
var closeButton = document.getElementById("close-button");
// Show the pop-up window when the link is clicked
popupLink.addEventListener("click", function(event) {
event.preventDefault();
popupWindow.style.display = "block";
});
// Hide the pop-up window when the close button is clicked
closeButton.addEventListener("click", function() {
popupWindow.style.display = "none";
}); */




/* const containerBox = document.getElementById('custom-file')
containerBox.innerHTML = '<ul class="filetree start"><li class="wait">' + 'Generating Tree...' + '<li></ul>'

const selectedFile = document.getElementById('custom-file')
selectedFile.innerHTML = '<ul class="filetree start"><li class="wait">' + 'Generating Tree...' + '<li></ul>'

$.ajax {
    type: 'GET'
    url: '/filebrowserJSON',
    success: function (response) {
        console.log('success', response.context)
        const data = response.context
        console.log(data)
        data.forEach(el=> {
            const entry = $(".class:contains('folder')" );
            containerBox.innerHTML += `
            ${}
        });

    },
    error: function(error) {
        console.log('error', error)
    }

} */
