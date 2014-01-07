$(document).ready(function() {
  $("div.enterleave")
  .mouseenter(function() {
              $(this).find(".hidden").css("display","block");
              $(this).css("border-bottom", "3px solid #022D71");
              })
  .mouseleave(function() {
              $(this).find(".hidden").css("display","none");
              $(this).css("border-bottom", "3px solid #fff");
              });
  
  });
