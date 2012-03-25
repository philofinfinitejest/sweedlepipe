%import random
%for key, value in groups.items():
%desc = value["description"]
%users = value["user_details"]
<div class="well">
<div class="row">
    <div class="span8"><h2>{{desc}}</h2></div><div class="span3"><a class="btn btn-primary" href="/generate">Group these suckas</a></div>
</div>
<div class="row"><div class="span11"><h4><a href="/groupdetails/{{key}}"screen_name"]}}">Why are these tweeters similar?</a></h1></div></div>
<div class="row">
    <div class="span11">
    %for user in users:
        %id = user["screen_name"] + str(random.randint(0,100))
        <a id="{{id}}" href="https://twitter.com/#!/{{user["screen_name"]}}" title="@{{user["screen_name"]}}" data-content="{{user["description"]}}"><img style="width: 48px;" src="{{user["profile_image_url"]}}"/></a>
    <script>
        $("#{{id}}").popover();
    </script>
    %end
    </div>
</div>
</div>
%end
%rebase layout


