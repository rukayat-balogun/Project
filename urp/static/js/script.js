// JavaScript Document for charity html template

$(document).ready(function() {
	
	
//open search bar toggle code

"use strict";
		// Search field toggle in top bar
		$('li.search a').click(function(e) {
			$(this).parent().find('#top-search').toggle().focus();
			$('#top-links').toggleClass('search-open');
			e.preventDefault();
		});
		
		
		// Client logo corousel
		"use strict";
		$("#owl-demo").owlCarousel({
		 autoPlay: 1000, //Set AutoPlay to 3 seconds
	  	 items : 4,
      itemsDesktop : [1199,2],
      itemsDesktopSmall : [979,2]
 
  });
// Testiminail  corousel
	"use strict";
	$("#owl-demo-testimonial").owlCarousel({
 
      autoPlay: 1000, //Set AutoPlay to 3 seconds
 
      items : 1,
      itemsDesktop : [1199,3],
      itemsDesktopSmall : [979,3]
 
  });	
  	/*
			 * Contact form
		 */
		 $("#contact-form").submit(function() {
		 	var form = $(this);
		 	var script = $(this).attr("action");
		 	$.ajax({
			 		type : "POST",
			 		url : script,
			 		dataType : "html",
			 		data : $(this).serialize(),
			 		beforeSend : function() {
			 			form.find('.loading').remove();
			 			form.find('.dynamic').append('<div class="loading"><i class="fa fa-3x fa-spinner fa-spin"></i></div>')
					},
					success : function(response) {
						form.find(".loading").remove();
			 			form.find('.dynamic').append('<div class="result">' + response + '</div>')
					}
			});
		 	return false;
		});
	
		
});

///////// javascipt form thankyou massage


function thanks() {
"use strict";
document.getElementById('thank').innerHTML = "<div class='alert alert-success' role='alert'> Thank you! Your message has been successfully sent. We will contact you very soon! </div>"; 
document.getElementById('thank_1').innerHTML = "<div class='alert alert-success' role='alert'> Thank you! Your message has been successfully sent. We will contact you very soon! </div>"; 
return true;
}

