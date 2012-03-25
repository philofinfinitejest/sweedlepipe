%if verified:
<p><h2>Welcome, @{{screen_name}}!</h2></p>
<p><a class="btn btn-primary btn-large" href="/generate">Let's do this &raquo;</a></p>
%else:
<p><h3>Press the button to be redirected to Twitter and tell them to let us know who you follow:</h3></p>
<p><a class="btn btn-primary btn-large" href="/login">Talk to Twitter &raquo;</a></p>
%end
%rebase layout
