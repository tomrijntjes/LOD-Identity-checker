function get_similar(){
            var uri = document.getElementById("url").value
            var format = "RDF"
            $.get('/get_similar',data={'uri': uri, 'format': format}, function(data){
                var responseString = "";
                for (URI in data) {
                    responseString += (URI + ": " + data[URI] + "<br>");
                }
                console.log(responseString);
                document.getElementById('response').innerHTML = responseString;
	    });
	
        }