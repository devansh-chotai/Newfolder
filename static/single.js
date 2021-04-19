var iframe = $("#iframeContent");
iframe.on("load",function ()
{
	iframe.contents().find("#nav").remove();
});

var donm = document.getElementById("donm");
var recm = document.getElementById("cart");
recm.onclick = function(e) {
	e.preventDefault();	
    donm.style.display = "block";
}

window.addEventListener("click", function(event) {
  if (event.target == donm) {
    donm.style.display = "none";
  }
});