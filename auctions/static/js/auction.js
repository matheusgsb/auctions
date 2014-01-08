$(document).ready(function(){
    var day, time;
    var timestamp = $("#date_end").html();
    timestamp = timestamp.split(" ");
    day = timestamp[0].split("/");
    time = timestamp[1].split(":");
    day = day.map(function(item){
       return parseInt(item);
    });
    time = time.map(function(item){
       return parseInt(item);
    });
  
    var date = new Date(2000 + day[2], day[1]-1, day[0], time[0], time[1], time[2], 0);
    $('#countdown').countdown({until: date});
    $("#bid").click(function(e) {
        if($("#id_value").val()==="")
        {
            alert("Please insert a valid value to place a bid.");
            e.preventDefault();
            return false;
        }
        var a = confirm("You're about to place a bid of "+$("#id_value").val()+" pounds. Are you sure?");
        if(a) {
            var form = $(this).parent();
            $.post( "/auction/"+$("#auction_id").val()+"/",form.serialize(), function( data ) {
                $("#success").html(data);
            }).fail(function(){
                alert("Your bid could not be placed, try again.")
            });
        } else
            alert("Bid cancelled.");
        e.preventDefault();
    });
});