$(document).ready(function(){
    var day, time;
    //Formating data entry to use on countdown
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
    //using the countdown plugin
    $('#countdown').countdown({until: date});
    //Validations before submission of the bid
    $("#bid").click(function(e) {
        //bid is required
        if($("#id_value").val()==="")
        {
            alert("Please insert a valid value to place a bid.");
            e.preventDefault();
            return false;
        }
        //ask for confirmation of the bid
        var a = confirm("You're about to place a bid of "+$("#id_value").val()+" pounds. Are you sure?");
        if(!a) 
        {
            alert("Bid cancelled.");
            e.preventDefault();
            return false;
        }
    });
});