$(document).ready(function(){
	$('input[type="number"]').on('change', function(){
		setTimeout(function(){
			$('#fade').fadeOut(400).fadeIn(100);
			$('#updateBtn').trigger('click');
		}, 500); 
	});
});

$('#submitOrder').on('click', function(e){
	e.preventDefault();
	window.location.href = "http://127.0.0.1:8000/orders/";

})

$('a.remove').click(function(){
	$( this ).parent().parent().parent().hide( 400 );
   
  })