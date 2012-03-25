<h2>Processing all your stuff...</h2>
<div class="progress progress-success">
  <div class="bar" id="progressbar" style="width:0%;"></div>
</div>

<script type="text/javascript">
$(document).ready( function() {
    var gengroups = $.getJSON("generategroups", function(json) { 
            window.location = "/groups"; 
        });
    var intervalId = setInterval(
        function() {
            //TODO: debug single call and no more
            if($("#progressbar").width() < 100) {
                $.ajax({  
                      url: "progress",  
                      dataType: "json",  
                      async: false,  
                      success: function(json) {$("#progressbar").width(json.progress + "%");}
                    });
            }
        },
        1000
    );
});
</script>
%rebase layout

