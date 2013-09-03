import os, psycopg2, urlparse, tweetpony, hashlib, time, requests_oauthlib

from requests_oauthlib import OAuth1Session

from bottle import route, run, template, get, post, request, static_file, error

#OKAY SERIOUSLY NEED TO LOOK INTO TEMPLATES OR SOMETHING
#GOT WAAAAAY TOO MUCH HTML GOING ON IN HERE

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]

def connecting():
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(
        database = url.path[1:],
	user = url.username,
	password = url.password,
	host = url.hostname,
	port = url.port
    )
    return conn

def save_string(str):
    connection = connecting()
    cur = connection.cursor()
    cur.execute("""INSERT INTO preteenify VALUES (%(trans)s)""", {'trans' : str})
    connection.commit()
    cur.close()
    connection.close()

def preteenify_tweet(str):
    # CONSUMER_KEY = os.environ["CONSUMER_KEY"]
    # CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
    api = tweetpony.API(
        consumer_key=CONSUMER_KEY, 
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    api.update_status(status = str)

def auth_url(CONSUMER_KEY, CONSUMER_SECRET):
    api = tweetpony.API(CONSUMER_KEY, CONSUMER_SECRET)
    url = api.get_auth_url()
    return url # put this url in the button link

def user_auth():
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    authentication_url = 'https://api.twitter.com/oauth/authenticate'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth_session = OAuth1Session(
        client_key=CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        callback_uri='http://0.0.0.0:5000/get-url'
        #update this before heroku push !
    )
    #first step
    oauth_session.fetch_request_token(request_token_url)
    #second step
    oauth_session.authorization_url(authentication_url)
    #third step
    resp = request.forms.get('redirect_response')
    oauth_session.parse_authorization_response(resp)
    oauth_session.fetch_access_token(access_token_url)
    return oauth_session

def user_tweet(oauth_session, new_string):
    status_url = 'https://api.twitter.com/1.1/statuses/update.json'
    new_status = {'status':  new_string}
    oauth_session.post(status_url, data=new_status)

@route('/')
def serve_index():
    #return static_file('index.html', root='static/')
    return '''<link rel=stylesheet type=text/css href="static/style.css">
              <title>
                PRETEENIFY
              </title>
              <body>
                <div class="header">
                  <h1 align = "center">
                    <a href="/">PRETEENIFY</a>
                  </h1>
                </div>
                <div class="translate">
                  <form method="POST" action="/translated" align="center">
                    <input name="word_string" type="text" maxlength="130"/>
                    <input type="submit" value="TRANSLATE"/>
                  </form>
                </div>
                <div class="twitter-login">
                  <a href ="''' + auth_url(CONSUMER_KEY, CONSUMER_SECRET) + '''">
                    <img src="static/sign-in-with-twitter-gray.png">
                  </a>
                </div>
                <div class="dolphin" align="top">
                  <img src="static/dolphin.gif">
                </div>
                <div class="palm" align="top">
                  <img src="static/palm.gif">
                </div>
                <div class="bieber" align="center">
                  <img src="static/leftJB.gif">
                </div>
                <div class="pizza" align="left">
                  <img src="static/adventurePIZZA.gif">
                </div>
                <div class="cat" align="right">
                  <img src="static/spacecat.gif">
                </div>
              </body>'''

@route('/get-url')
def get_info():
    return '''<link rel=stylesheet type=text/css href="static/style.css">
              <title>
                PRETEENIFY
              </title>
              <body>
                <div class="header">
                  <h1 align = "center">
                    <a href="/">PRETEENIFY</a>
                  </h1>
                </div>
                <!--<div class="translate">
                  <form method="POST" action="/translated" align="center">
                    <input name="word_string" type="text" maxlength="130"/>
                    <input type="submit" value="TRANSLATE"/>
                  </form>
                </div>-->
                <div class="twitter-code">
                  <!--<form method="GET" action="/" align="center">-->
                  <form method="POST" action="/translated" align="center">
                    <input name="redirect_response" type="text" value="ENTER URL"/>
                    <input name="word_string" type="text" value="ENTER STUFF TO BE TRANSLATED" maxlength="130"/>
                    <input type="submit" value="TRANSLATE"/>
                    <!--<input type="submit" value="ENTER URL"/>-->
                  </form>
                </div>
                <div class="dolphin" align="top">
                  <img src="static/dolphin.gif">
                </div>
                <div class="palm" align="top">
                  <img src="static/palm.gif">
                </div>
                <div class="bieber" align="center">
                  <img src="static/leftJB.gif">
                </div>
                <div class="pizza" align="left">
                  <img src="static/adventurePIZZA.gif">
                </div>
                <div class="cat" align="right">
                  <img src="static/spacecat.gif">
                </div>
              </body>'''

@route('/get-pin')
def get_info():
    return '''<link rel=stylesheet type=text/css href="static/style.css">
              <title>
                PRETEENIFY
              </title>
              <body>
                <div class="header">
                  <h1 align = "center">
                    <a href="/">PRETEENIFY</a>
                  </h1>
                </div>
                <div class="twitter-code">
                  <form method="GET" action="/" align="center">
                    <input name="pin_code" type="text"/>
                    <input type="submit" value="ENTER PIN"/>
                  </form>
                </div>
                <div class="dolphin" align="top">
                  <img src="static/dolphin.gif">
                </div>
                <div class="palm" align="top">
                  <img src="static/palm.gif">
                </div>
                <div class="bieber" align="center">
                  <img src="static/leftJB.gif">
                </div>
                <div class="pizza" align="left">
                  <img src="static/adventurePIZZA.gif">
                </div>
                <div class="cat" align="right">
                  <img src="static/spacecat.gif">
                </div>
              </body>'''

#HELL YEAH USER TWEETS ARE GOOOOOO!
@post('/translated')
def serve_translation():
    word_string = request.forms.get('word_string')
    new_string = translate(word_string)
    save_string(new_string)
    #NEED TO SEPARATE CODE HERE (preteenify_tweet goes somewhere...)
    oauth_session = user_auth()
    user_tweet(oauth_session, new_string)
    user_name = 'my_name'
    return '''<link rel=stylesheet type=text/css href="static/style.css">
              <title>
                PRETEENIFY
              </title>
	      <body>
                <div class="header">
    	        <h1 align = "center">
      		  <a href="/">PRETEENIFY</a>
    		</h1>
                </div>
    		<div class="words">
		'''+ new_string +'''</div>
    		<div class="dolphin" align="top">
      		  <img src="static/dolphin.gif">
    		</div>
    		<div class="palm" align="top">
      		  <img src="static/palm.gif">
    		</div>
                <!-- OKAY OBVIOUSLY THIS DOESN'T WORK BUT YEAH -->
    		<div class="bieber" align="center">
                  <a class="twitter-timeline" width="300" height="450" href="https://twitter.com/''' + user_name + ''' "  data-widget-id="364628094939717632">Tweets by @''' + user_name + ''' </a>
                  <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
    		</div>
    		<div class="pizza" align="left">
      		  <img src="static/adventurePIZZA.gif">
    		</div>
    		<div class="cat" align="right">
                  <img src="static/spacecat.gif">
    		</div>
  	      </body>'''
#this is where the preteenify_tweet else clause used to be

def translate(word_string):

    vocab_dict = {
        'to' : '2',
        'too' : '2',
        'for' : '4',
	'ate' : '8',
	'you' : 'u',
	'thanks' : 'thx',
	'please' : 'plz',
	'love' : 'luv',
	'haha' : 'lol',
	'oh my god' : 'omg',
	'ight' : 'ite',
	'girl' : 'gurl',
	'and' : '&',
	'because' : 'cuz',
	'forever' : '4ever',
	'what' : 'wut',
        'house' : 'haus',
        'thing' : 'thang',
    } 

    for key in vocab_dict:
        if key in word_string:
	    word_string = word_string.replace(key, vocab_dict[key])

    words = word_string.split(" ")
    count = 0
    index = 0

    for each in words:
        each = each.lower()
        for letter in each:
	    count+=1
	    if count % 2 == 0:
	        each = each.replace(letter, letter.upper())
        words[index] = each
	index+=1
    return '((~* ' + ' '.join(words) + ' *~))'

@route('/static/<filename>')
def serve_style(filename='style.css'):
    return static_file(filename, root='static/')

@get('/favicon.ico')
def serve_favicon():
    return static_file('favicon.ico', root='static/')
    #only works for static icon in chrome?

@error(404)
def error404(error):
    return '''<link rel=stylesheet type=text/css href="static/style.css">
              <title>
                PRETEENIFY
              </title>
              <body>
                <h1 align = "center">
                  <a href="/">PRETEENIFY</a>
                </h1>
                <div class="sad">
                  <img src="static/sad_dawson.gif">
                </div>
                <div class="msg">
                  YOU BROKE THE WEBSITE BRO
                </div>
              </body>'''

@error(500)
def error500(error):
    word_string = request.forms.get('word_string')
    return '''<link rel=stylesheet type=text/css href="static/style.css">
              <title>
                PRETEENIFY
              </title>
              <body>
                <h1 align = "center">
                  <a href="/">PRETEENIFY</a>
                </h1>
                <div class="trans">
                  SOMETHING TERRIBLE HAPPENED:
                  <br>HERE\'S YOUR TRANSLATION 
                  <p>''' + translate(word_string) + '''
		</div>
                <div class="lindsay">
                  <img src="static/lindsay_palm.gif">
                </div>
              </body> '''

run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
#heroku setting

#run(host='localhost', port=8080, debug=True)
#local dev setting
