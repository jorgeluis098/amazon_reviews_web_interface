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
                $("#result-text").html(response["result"]);
                
            },
            error: function(error){
				console.log("Error");
                //set_modal(error);
                //$("#js-loader").css("display","none");
            }
        }); 
    });
    graphs();
    function graphs (data){
            var ctx = document.getElementById('myChart');
            var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Negativos', 'Positivos'],
                datasets: [{
                    label: 'Numero de comentarios',
                    data: [12, 19],
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


