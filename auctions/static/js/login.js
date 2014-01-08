//used to avoid empty inputs
$(document).ready( function() {
                  //login form - header
                  $('#submit_login').click(function(e){
                                     if ($('#username_login').val() === "" || $('#password_login').val()==="") {
                                     $('#error_login').html("<b>Error:</b> All the fields are required!");
                                     e.preventDefault();
                                     }
                                     });
                  //login form - login.html
                  $('#submit_page').click(function(e){
                                     if ($('#username_page').val() === "" || $('#password_page').val()==="") {
                                     $('#error_page').html("<b>Error:</b> All the fields are required!");
                                     e.preventDefault();
                                     }
                                     });
                  });