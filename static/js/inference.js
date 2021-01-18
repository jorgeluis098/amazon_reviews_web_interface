$(document).ready(function (){

    $('#inference-text-btn').on('click', function (e) {
		e.preventDefault()
		var formData = new FormData();
		formData.append("card_text", $("#card_text").val())
        $.ajax({
            url: '/inference_text',
            data: formData,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                console.log(response);
            },
            error: function(error){
				console.log("Error");
                //set_modal(error);
                //$("#js-loader").css("display","none");
            }
        }); 
    });



});


