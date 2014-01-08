// used to display the hidden div of each auction item
$(document).ready(function() {
  $("div.enterleave")
  .mouseenter(function() {
              //when the mouse enter, change the display to block
              $(this).find(".hidden").css("display","block");
              $(this).css("border-bottom", "3px solid #022D71");
              })
  .mouseleave(function() {
              //when it leaves, change it to the hidden mode again
              $(this).find(".hidden").css("display","none");
              $(this).css("border-bottom", "3px solid #fff");
              });
  
  });
