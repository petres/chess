var possibleMoves = {};

function boardUpdate(data) {
	possibleMoves = {}
	$.each( data['board'], function(id, val) {
		if(val) {
			$("#chessBoard td#" + id).html("<span class='cp " + val.color + " " + val.piece + "'></span>")
			possibleMoves[id] = val.possibleMoves
		} else {
			$("#chessBoard td#" + id).html("")
		}
	});
}

function restart() {
	$.getJSON( "/restart", function(data) {
		boardUpdate(data)
	});
}

function move(origin, target) {
	$.getJSON( "/move/" + origin + "/" + target, function(data) {
		boardUpdate(data)
	});
}

var first = null
$( function() {
	restart()
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
})