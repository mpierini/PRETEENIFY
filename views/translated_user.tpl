    <div class="again">
      <form method="POST" action="/translated_user" align="center">
        <input name="word_string" type="text" value="ENTER STUFF TO BE TRANSLATED" maxlength="130"/>
        <input type="submit" value="TRANSLATE"/>
      </form>
    </div>
    <div class="words">
      {{new_string}}
    </div>
    <div class="twitter-login">
      <form method="GET" action="/signed-out" align="center">
        <input name="logged_out" type="submit" value="SIGN OUT!"/>
      </form>
    </div>
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
    %rebase layout

