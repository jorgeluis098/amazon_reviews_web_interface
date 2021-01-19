$(document).ready(function (){

    graphs();

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
				$("#result").text(response["result"]);
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
            },
            error: function(error){
				console.log("Error");
            }
        }); 
    });

    
    function graphs (){
            var ctx = document.getElementById('myChart');
            var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Red', 'Blue'],
                datasets: [{
                    label: '# of Votes',
                    data: [12, 19],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
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


