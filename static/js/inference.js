$(document).ready(function (){

    graphs();

    $('#inference-text-btn').on('click', function (e) {
        e.preventDefault()
        $('#imagen-positiva').removeClass('d-block').addClass('d-none');
        $('#imagen-negativa').removeClass('d-block').addClass('d-none');
		var formData = new FormData();
		formData.append("card_text", $("#card_text").val())
        $.ajax({
            url: '/inference_text',
            data: formData,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                if (response["result"]=="Negativo"){
                    $('#imagen-negativa').removeClass('d-none').addClass('d-block');
                } else {
                    $('#imagen-positiva').removeClass('d-none').addClass('d-block');
                    
                }
            },
            error: function(error){
				console.log("Error");
            }
        }); 
    });

	
    $('#file-inference-btn').on('click', function (e) {
		e.preventDefault()
		var form_data = new FormData($('#analize-file-form')[0]);
        $.ajax({
            url: '/inference_file',
            data: form_data,
            type: 'POST',
            contentType: false,
            processData: false,
            success: function(response){
                /*
                response["sentiment_data"] = number
                response["img_positive"] = get_wordcloud(topics_positive)
                response["img_negative"] = get_wordcloud(topics_negative)
                */
                //$("#result").text(response["result"]);
                $("#resultado-2").html(response["img_positive"])
                $("#resultado-3").html(response["img_negative"])
                graphs(response["sentiment_data"]);
            },
            error: function(error){
				console.log("Error");
            }
        }); 
    });

    
    function graphs (data){
            var ctx = document.getElementById('myChart');
            var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Negativos', 'Positivos'],
                datasets: [{
                    label: 'Numero de comentarios',
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.3)',
                        'rgba(25, 135, 84, 0.3)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(25, 135, 84, 1)'
                    ],
                    borderWidth: 0.5
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }
});


