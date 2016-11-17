$( document ).ready(function() {
var clickedNotify = false;
//$('p a').tooltip({placement: 'bottom'}).tooltip('show');
$('.linkTT').mouseleave(function() { if (!clickedNotify) { $('p a').tooltip({placement: 'bottom'}).tooltip('show'); } });
$('.linkTT').click(function() { clickedNotify = true; $(this).tooltip('destroy'); });
});


var getString=function(){
	getAString("HEL");
	getAString("AGDISTIS");
}

var getAString=function(sys){
	var reqUrl = "http://flask.fii800.eculture.labs.vu.nl/" + sys + "/" + $("#docnum").val();
	console.log(reqUrl);
	$.get(reqUrl, function(response, status){
		text=response['s'];
		var e=response['tps'];
		for (var i=0; i<e.length; i++){
			var entities=e[i];
			if (entities[2]=="true") var color="green";
			else var color="red";
			if (entities[4]!="") var conf="Confidence: " + entities[4] + "\n";
			else var conf="Confidence: NIL\n";
			var golden="";
			if (entities[5] && !entities[5].includes("vu.nl/unknown"))
				golden="GOLD: " + entities[5];
			else
				golden="GOLD: " + entities[3];
			if (!entities[3].includes("vu.nl/unknown"))
				var system=entities[3];
			else
				var system="EMERGING ENTITY";
			if (sys=="HEL"){
				text=text.substring(0, entities[0]) + '<a class="linkTT" style="color:black" data-toggle="tooltip" data-placement="top" title="SYSTEM: ' + system +'\n' + conf + golden + '"  href="' + entities[3] + '"><span style="background-color:' + color + ';">' + text.substring(entities[0], entities[1]) + '</span></a>' + text.substring(entities[1]);
			} else{
                                text=text.substring(0, entities[0]) + '<a class="linkTT" style="color:black" data-toggle="tooltip" data-placement="top" title="SYSTEM: ' + system +'\n' + golden + '"  href="' + entities[3] + '"><span style="background-color:' + color + ';">' + text.substring(entities[0], entities[1]) + '</span></a>' + text.substring(entities[1]);

                                //text=text.substring(0, entities[0]) + '<span style="background-color:' + color + ';">' + text.substring(entities[0], entities[1]) + '</span>' + text.substring(entities[1]);
			}
		}
		if (sys=="HEL"){
			$("#myText").html(text);
		} else {
			$("#AGDISTISText").html(text);
		}
	})
}
