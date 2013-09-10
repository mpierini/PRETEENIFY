    <div class="words">
      {{new_string}}
    </div>
    %import os
    %if os.path.isfile('./secret_session'):
    <div class="twitter-login">
      <form method="GET" action="/signed-out" align="center">
        <input name="logged_out" type="submit" value="SIGN OUT!"/>
      </form>
    %end 
    </div>
    <div class="timeline" align="center">
      <a class="twitter-timeline" width="300" height="450" href="https://twitter.com/"{{user_name}} data-widget-id="364628094939717632">Tweets by @{{user_name}}
      </a>
      <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");
      </script>
    </div>
    %rebase layout
