$(document).ready(function()
	{
		//function to validate date extracted from http://jsfiddle.net/jquerybyexample/EywSP/
		function isDate(txtDate)
		{
			var currVal = txtDate;
			if(currVal === '')
				return false;
			//Declare Regex  
			var rxDatePattern = /^(\d{1,2})(\/|-)(\d{1,2})(\/|-)(\d{4})$/; 
			var dtArray = currVal.match(rxDatePattern); // is format OK?

			if (dtArray === null)
				return false;
			//Checks for mm/dd/yyyy format.
			var dtMonth = dtArray[1];
			var dtDay= dtArray[3];
			var dtYear = dtArray[5];
			if (dtMonth < 1 || dtMonth > 12)
				return false;
			else if (dtDay < 1 || dtDay> 31)
				return false;
			else if ((dtMonth==4 || dtMonth==6 || dtMonth==9 || dtMonth==11) && dtDay ==31)
				return false;
			else if (dtMonth == 2)
			{
				var isleap = (dtYear % 4 === 0 && (dtYear % 100 !== 0 || dtYear % 400 === 0));
				if (dtDay> 29 || (dtDay ===29 && !isleap))
					return false;
			}
			return true;
		}

		//masking the input for date
		$("#id_date_end").mask("99/99/9999 99:99");
		
		//adding class editable for all the inputs and select
		$("input").addClass("editable");
		$("select").addClass("editable");
		$("#confirm").click(function(e)
		{
			var flag = true;
			//validating inputs before submission
			$("#auction_form").find("input").each(function()
			{
				//all inputs are required
				if($(this).attr("type") !== "file" && $(this).val() === "")
				{	
					alert($(this).attr("placeholder")+" is required");
					flag=false;
					return false;
				}
				//image upload is also required
				if($(this).attr("id")==="id_p_image" && $(this).val() === "")
				{
					alert("Please upload an image");
					flag=false;
					return false;
				}

				if($(this).attr("id")==="id_date_end")
				{
					//spliting date on the format dd/mm/yyyy hh:mm between date and time
					//the date is validated using the function above
					//hours can't be bigger than 23 and minutes can't be bigger than 59
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
					//starting price should be a valid number
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
				e.preventDefault();
				return; 
			}
		});
		$("select").each(function()
		{
			$("#"+$(this).attr("name")).html($(this).find(":selected").text());
		});
		//when the inputs or selects change their values
		//are updated on the Confirmation tag
		$(".editable").change(function()
		{
			if(!$(this).is("select"))
				$("#"+$(this).attr("name")).html($(this).val());
			else
				$("#"+$(this).attr("name")).html($(this).find(":selected").text());
		});

		//the four functions above are for the navigation
		//between the steps on the progressbar
		$("#next1").click(function()
		{
			var next = $(this).parent().next();
			//activate next fieldset based on the index
			$("#progressbar li").eq($("fieldset").index(next)).addClass("active");
			$("#product_info").css("display","none");
			$("#auction_info").css("display","block");
		});
		$("#next2").click(function()
		{
			var next = $(this).parent().next();
			//activate next fieldset based on the index
			$("#progressbar li").eq($("fieldset").index(next)).addClass("active");
			$("#auction_info").css("display","none");
			$("#confirmation").css("display","block");
		});
		$("#previous1").click(function()
		{
			var curr = $(this).parent();
			//activate previous fieldset based on the index
			$("#progressbar li").eq($("fieldset").index(curr)).removeClass("active");
			$("#auction_info").css("display","none");
			$("#product_info").css("display","block");
		});
		$("#previous2").click(function()
		{
			var curr = $(this).parent();
			//activate previous fieldset based on the index
			$("#progressbar li").eq($("fieldset").index(curr)).removeClass("active");
			$("#confirmation").css("display","none");
			$("#auction_info").css("display","block");
		});
	});