    <div class="translate">
      <form method="POST" action="/translated" align="center">
        <input name="word_string" type="text" maxlength="130"/>
        <input type="submit" value="TRANSLATE"/>
      </form>
    </div>
    %import os
    %if not os.path.isfile('./secret_session'): 
    <div class="twitter-login">
      <a href = {{url}}>
        <img src="static/sign-in-with-twitter-gray.png">
      </a>
    </div>
    %else:
    <div class="twitter-login">
      <form method="GET" action="/signed-out" align="center">
        <input name="logged_out" type="submit" value="SIGN OUT!"/>
      </form>
    </div>
    %end
    %rebase layout 
