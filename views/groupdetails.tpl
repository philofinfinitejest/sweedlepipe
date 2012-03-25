%import random
<div class="well">
<div class="row">
    <div class="span8"><h2>These ones<h2></div>
</div>
<div class="row">
    <div class="span11">
    %for user in user_details:
        <a id="{{user["screen_name"]}}" href="https://twitter.com/#!/{{user["screen_name"]}}" title="@{{user["screen_name"]}}" data-content="{{user["description"]}}"><img style="width: 48px;" src="{{user["profile_image_url"]}}"/></a>
    <script>
        $("#{{user["screen_name"]}}").popover();
    </script>
    %end
    </div>
</div>
</div>
<div class="well">
<div class="row">
    <div class="span8"><h2>have these ones in common<h2></div>
</div>
<div class="row">
    <div class="span11">
    %for user in similarities:
        %id = user["screen_name"] + str(random.randint(0,100))
        <a id="{{id}}" href="https://twitter.com/#!/{{user["screen_name"]}}" title="@{{user["screen_name"]}}" data-content="{{user["description"]}}"><img style="width: 40px;" src="{{user["profile_image_url"]}}"/></a>
    <script>
        $("#{{id}}").popover();
    </script>
    %end
    </div>
</div>
</div>
%rebase layout


