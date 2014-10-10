var possibleMoves = {};

function boardUpdate(data) {
	possibleMoves = {}
	$.each(data['board'], function(id, val) {
		if(val) {
			$("#chessBoard td#" + id).html("<span class='cp " + val.color + " " + val.piece + "'></span>")
			possibleMoves[id] = val.possibleMoves
		} else {
			$("#chessBoard td#" + id).html("")
		}
	});
	$("#chessBoard td").removeClass("lastMove")
	$.each(data['lastMove'], function(id, val) {
		$("#chessBoard td#" + val).addClass("lastMove")
	});
	var statusMessage = "Turn of " + data['turnOf'] + "."
	if(data['over']) {
		statusMessage = "Game is over!"
		if(data['check']) 
	 		statusMessage += " Check Mate,  " + data['turnOf'] + " lost!"
	 	else
	 		statusMessage += " Stale Mate!"
	} else if(data['check']) {
		statusMessage = "Check! " + statusMessage;
	}
	$("#status").html(statusMessage)
}

function restart() {
	$.getJSON("/restart", function(data) {
		boardUpdate(data)
	});
}

function move(origin, target) {
	$.getJSON("/move/" + origin + "/" + target, function(data) {
		boardUpdate(data)
	});
}

var first = null
$( function() {
	$.getJSON("/getBoardInfo", function(data) {
		boardUpdate(data)
	});
	$("#chessBoard td").click( function() {
		if(!first) {
			var id = $(this).attr("id")
			$("#chessBoard td#" + id).addClass("marked")
			for(field in possibleMoves[id]) {
				$("#chessBoard td#" + possibleMoves[id][field]).addClass("possibleTargetField")
			}
			first = id
		} else {
			var id = $(this).attr("id")
			if($(this).hasClass("possibleTargetField")) {
				move(first, $(this).attr("id"))
			} 
			$("#chessBoard td").removeClass("marked")
			$("#chessBoard td").removeClass("possibleTargetField")
			first = null
		}
	});

	$("#ki").change(function () {
		$.getJSON("/changeKI/" + $(this).val(), function(data) {
			if(data)
				alert("KI changed")
		});
	});
})