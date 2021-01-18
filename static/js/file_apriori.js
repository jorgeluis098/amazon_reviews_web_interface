$(document).ready(function (){
	// $("#button_apriory").click(function(){
	// 	console.log("Hola bebe");
	// 	event.preventDefault();
	// });

	$("#button_apriory").click(function(){
		var formData = new FormData($('#form_apriori')[0]);
		console.log("Hola bebe entre a leer el archivo");
		$.ajax({
			url: '/read_apriori',
			data: formData,
			type: 'POST',
			contentType: false,
			processData: false,
			success: function(response){
				$("#table_values").html(response["sel_columns_html"]);
				$("#head_table").html(response["head"]);
				columns = response["columns"];
				$("#features-container").css("display","block");
				
			},
			error: function(error){
				console.log(error);
				event.preventDefault();
			}
		});    
	});


});


