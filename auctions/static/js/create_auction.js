$(document).ready(function()
	{
		$("input").addClass("editable");
		$("select").addClass("editable");
		$("select").each(function()
		{
			$("#"+$(this).attr("name")).html($(this).val());
		});
		$(".editable").change(function()
		{
			$("#"+$(this).attr("name")).html($(this).val());
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