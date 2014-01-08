$(document).ready(function()
	{
		function isDate(txtDate)
		{
		  var currVal = txtDate;
		  if(currVal == '')
		    return false;
		  
		  //Declare Regex  
		  var rxDatePattern = /^(\d{1,2})(\/|-)(\d{1,2})(\/|-)(\d{4})$/; 
		  var dtArray = currVal.match(rxDatePattern); // is format OK?

		  if (dtArray == null)
		     return false;
		 
		  //Checks for mm/dd/yyyy format.
		  dtMonth = dtArray[1];
		  dtDay= dtArray[3];
		  dtYear = dtArray[5];

		  if (dtMonth < 1 || dtMonth > 12)
		      return false;
		  else if (dtDay < 1 || dtDay> 31)
		      return false;
		  else if ((dtMonth==4 || dtMonth==6 || dtMonth==9 || dtMonth==11) && dtDay ==31)
		      return false;
		  else if (dtMonth == 2)
		  {
		     var isleap = (dtYear % 4 == 0 && (dtYear % 100 != 0 || dtYear % 400 == 0));
		     if (dtDay> 29 || (dtDay ==29 && !isleap))
		          return false;
		  }
		  return true;
		}
		$("#id_date_end").mask("99/99/9999 99:99");
		
		$("input").addClass("editable");
		$("select").addClass("editable");
		$("#confirm").click(function(e)
		{
			var flag = true;
			$("#auction_form").find("input").each(function()
			{
				if($(this).attr("type") != "file" && $(this).val() === "")
				{	
					alert($(this).attr("placeholder")+" is required");
					flag=false;
					return false;
				}
				if($(this).attr("id")==="id_p_image" && $(this).val() === "")
				{
					alert("Please upload an image");
					flag=false;
					return false;
				}
				if($(this).attr("id")==="id_date_end")
				{
					var val = $(this).val().split(" ");
					var time = val[1].split(":");
					if(!isDate(val[0]) || time[0]>23 || time[1]>59)
					{
						alert("The end date is invalid!");
						flag=false;
						return false;
					}
				}
				if($(this).attr("id")==="id_start_price")
				{
					if(isNaN($(this).val()) || $(this).val()<0)
					{
						alert("Invalid starting price!");
						flag=false;
						return false;
					}
				}
			});
			if(flag)
				$("#auction_form").submit();
			else
			{
				return; 
				e.preventDefault();
			}
		});
		$("select").each(function()
		{
			$("#"+$(this).attr("name")).html($(this).find(":selected").text());
		});
		$(".editable").change(function()
		{
			if(!$(this).is("select"))
				$("#"+$(this).attr("name")).html($(this).val());
			else
				$("#"+$(this).attr("name")).html($(this).find(":selected").text());
		});
		$("#next1").click(function()
		{
			next_fs = $(this).parent().next();
	
			//activate next step on progressbar using the index of next_fs
			$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
			$("#product_info").css("display","none");
			$("#auction_info").css("display","block");
		});
		$("#next2").click(function()
		{
			next_fs = $(this).parent().next();
	
			//activate next step on progressbar using the index of next_fs
			$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
			$("#auction_info").css("display","none");
			$("#confirmation").css("display","block");
		});
		$("#previous1").click(function()
		{
			current_fs = $(this).parent();
	
			//de-activate current step on progressbar
			$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
			$("#auction_info").css("display","none");
			$("#product_info").css("display","block");
		});
		$("#previous2").click(function()
		{
			current_fs = $(this).parent();
	
			//de-activate current step on progressbar
			$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
			$("#confirmation").css("display","none");
			$("#auction_info").css("display","block");
		});
	});