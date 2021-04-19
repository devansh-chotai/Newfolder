$('#submitOrder').on('click', function(e){
	// e.preventDefault();
	var x = $('#totalPrice').text();
	var totalPrice = parseInt(x);
	var y = document.getElementById('balance').value;
	var Balance = parseInt(y);
	console.log(Balance);
	console.log(totalPrice);
	if(totalPrice <= Balance){
		console.log('ordered sucessfully')
		Balance=Balance-totalPrice
		console.log(Balance)
		window.location.href = "http://127.0.0.1:8000/orders/history";
	}
	else{
		e.preventDefault();
		document.getElementById("lowBalance").classList.remove("hidden");;
	}
})

var donm = document.getElementById("donm");
var cls = document.getElementById("cancel");
var recm = document.getElementById("form");
recm.onclick = function(e) {
	e.preventDefault();	
    donm.style.display = "block";
}

cls.onclick = function() {
  donm.style.display = "none";
}

window.addEventListener("click", function(event) {
  if (event.target == cls) {
    donm.style.display = "none";
  }
});