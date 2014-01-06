function validateEmail(email) { 
  // http://stackoverflow.com/a/46181/11236
  
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}
    $(document).ready(function()
    {

      $("#register").click(function(e)
      {
        if($("#id_username").val()==="")
        {
          alert("Insert an username");
          e.preventDefault();
          return;
        }
        if(!validateEmail($("#id_email").val()))
        {
          alert("Invalid e-mail");
          e.preventDefault();
          return;
        }
        if($("#id_password1").val()!=$("#id_password2").val())
        {
          alert("The passwords are different");
          e.preventDefault();
          return;
        }
        if($("#id_password1").val().length >15
          || $("#id_password2").val().length >15)
        {
          alert("Password too long");
          e.preventDefault();
          return;
        }
        if($("#id_password1").val().length <6
          || $("#id_password2").val().length <6)
        {
          alert("Password too short");
          e.preventDefault();
          return;
        }
      })
    });