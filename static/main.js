$(document).ready(function(){
    $('#fademessage').delay(6000).fadeOut(300);
});

// $("#pd").on("keyup keypress", function(e){
//     console.log(e.keyCode)
//     var kk = e.keyCode || e.which;
//     if(e.keyCode == 13){
//         e.preventDefault();
//         console.log("hola")
//         return false;
//     }
//     else{
//         console.log("dwedwe")
//     }
//  });

 $(window).ready(function() {
    $("#pd").on("keypress", function (event) {
        var keyPressed = event.keyCode || event.which;
        if (keyPressed === 13) {
            event.preventDefault();
            $("#trigger").trigger("click");
            return false;
        }
    });
    });