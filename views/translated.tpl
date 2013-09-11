    <div class="words">
      {{new_string}}
    </div>
    %import os
    %if os.path.isfile('./secret_session'):
    <div class="twitter-login">
      <form method="GET" action="/signed-out" align="center">
        <input name="logged_out" type="submit" value="SIGN OUT!"/>
      </form> 
    </div>
    %end
    %if not os.path.isfile('./secret_session'):
    <div class="timeline" align="center">
      <a class="twitter-timeline" width="300" height="450" href="https://twitter.com/"{{user_name}} data-widget-id="364628094939717632">Tweets by @{{user_name}}
      </a>
      <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");
      </script>
    </div>
    %else:
    <div class="user-header">
      <p>
        <a class="twitter-timeline" width="300" height="450" href="https://twitter.com/{{user_name}}">Tweets by @{{user_name}}
        </a>
      </p>
      %user_img = tweets[0]['user']['profile_image_url']
      <div class="img">
        <img src="{{user_img}}"></img>
      </div>
    </div>
    %img_url = tweets[0]['user']['profile_background_image_url']
    <div class="user-timeline" style="background-image:url({{img_url}});">
      %for item in tweets:
        <div class="tweet">
          <p>{{item['text']}}</p>
        </div>
      %end
    </div>
    %end
    %rebase layout
