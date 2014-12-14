
var rapView = {
  'config' : {
    'upvote_button' : $('.up'),
    'downvote_button' : $('.down'),
    'tooltip' : $('[data-toggle="popover"]')
  },
  'init' : function(config) {
    if (config && typeof(config) == 'object') {
          $.extend(rapView.config, config);
    }
    rapView.$upvote = rapView.config.upvote_button;
    rapView.$downvote = rapView.config.downvote_button;
    rapView.$tooltip = rapView.config.tooltip

    var upvote = rapView.upvote(rapView.$upvote);
    var downvote = rapView.downvote(rapView.$downvote);
    var tooltip = rapView.tooltip(rapView.$tooltip);

    rapView.initialized = true;
  },
  'tooltip' : function($tooltip) {
    $tooltip.popover({html:true});
    $tooltip.on('click', function(e) {
      $tooltip.not(this).popover('hide');
    });
  },
  'upvote' : function($upvote) {
    $upvote.click(function(){
      var line_id = $(this).parents(".votes").attr("id").split("number")[1];
      rapView.sendRequest(line_id, "upvote", this); 
    });
  },
  'downvote' : function($downvote) { 
    $downvote.click(function(){
      var line_id = $(this).parents(".votes").attr("id").split("number")[1];
      rapView.sendRequest(line_id, "downvote", this); 
    });
  },
  'sendRequest' : function(line_id, vote_type, vote_ele) {
    $.post( "/line/_" + vote_type, { 'lineID' : line_id } )
      .success(function( data ) {
        if (data["Success"] === true) {  
          constructor = "#number" + line_id;
          $(constructor + " i").css({"color" : "#dddddd" });
          $(constructor + " i").addClass("voted");
          if (vote_type === "upvote") {
            var current_val = parseInt($(constructor + " .up_count").text());
            $(constructor + " .up_count").text(current_val + 1);
          }
          else if (vote_type==="downvote") {
            var current_val = parseInt($(constructor + " .down_count").text());
            $(constructor + " .up_count").text(current_val + 1);
          }
        location.reload();
        }
    });
  }
}

