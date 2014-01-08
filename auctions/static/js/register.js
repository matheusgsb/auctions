function validateEmail(email) { 
  // http://stackoverflow.com/a/46181/11236
  
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}
    $(document).ready(function()
    {
      $("#register").click(function(e)
      {
        var error_msg = "<b>Error(s):</b><br>";
        if($("#id_username").val()==="")
        {
          error_msg += " *Insert an username<br>";
          e.preventDefault();
        }
        if(!validateEmail($("#id_email").val()))
        {
          error_msg += " *Invalid e-mail<br>";
          e.preventDefault();
        }
        if($("#id_password1").val()!=$("#id_password2").val())
        {
          error_msg += " *The passwords are different<br>";
          e.preventDefault();
        }
        if($("#id_password1").val().length >15 || $("#id_password2").val().length >15)
        {
          error_msg += " *Password too long<br>";
          e.preventDefault();
        }
        if($("#id_password1").val().length <6 || $("#id_password2").val().length <6)
        {
          error_msg += " *Password too short<br>";
          e.preventDefault();
        }
        if(error_msg != "<b>Error(s):</b><br>") {
            $("#error").html(error_msg);
            return false;
        }
      });
    });