    <script type="text/javascript">
      function ShowPopup(hoveritem)
      {   
        hp = document.getElementById("hoverpopup");
        // Set popup to visible
        hp.style.visibility = "Visible";
      }

      function HidePopup()
      {
        hp = document.getElementById("hoverpopup");
        hp.style.visibility = "Hidden";
      } 
    </script>

    <div class="what">
      <a style="cursor:default;" onMouseOver="ShowPopup(this);" onMouseOut="HidePopup();">WhAt's gOiNg oN HeRE?!</a>
      <div class="explain" id="hoverpopup">
        Translate a line of text and tweet it out to the
        <a href="https://twitter.com/PRETEENIFY">@PRETEENIFY</a>
        account. Or click the sign in with Twitter button to tweet your 
        translation to your own Twitter account. You need to paste the
        current url into the form where prompted. Raw text goes below
        and then hit TRANSLATE.
      </div>
    </div>
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
