import os, psycopg2, urlparse, tweetpony, requests_oauthlib, pickle 

from requests_oauthlib import OAuth1Session

from bottle import route, run, template, get, post, request, static_file, error, redirect

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
    AUTH_URL = api.get_auth_url()
    return AUTH_URL # put this url in the button link

#saving tokens - is secure ish?
def save_secrets(filename, token):
    f = open(filename, 'w')
    pickle.dump(token, f)
    f.close()

def access_secrets(filename):
    f = open(filename, 'r')
    token = pickle.load(f)
    f.close()
    return token

def user_auth():
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    authentication_url = 'https://api.twitter.com/oauth/authenticate'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth_session = OAuth1Session(
        client_key=CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        #callback_uri='http://preteenify.herokuapp.com/get-url'
        callback_uri='http://0.0.0.0:5000/get-url'
    )
    #first step
    oauth_session.fetch_request_token(request_token_url)
    #second step
    oauth_session.authorization_url(authentication_url)
    #third step
    resp = request.forms.get('redirect_response')
    oauth_session.parse_authorization_response(resp)
    token = oauth_session.fetch_access_token(access_token_url)
    save_secrets('secret_token', token)
    save_secrets('secret_session', oauth_session)

def user_tweet(oauth_session, new_string):
    status_url = 'https://api.twitter.com/1.1/statuses/update.json'
    new_status = {'status':  new_string}
    oauth_session.post(status_url, data=new_status)

def user_timeline(oauth_session, user_name):
    timeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    timeline_url += '?screen_name='
    timeline_url += user_name
    timeline_url += '&count=10'
    tweets = oauth_session.get(timeline_url)
    return tweets #returns list thing

@route('/')
def serve_index():
    url =  auth_url(CONSUMER_KEY, CONSUMER_SECRET)
    return template('index', url=url)
    
@route('/get-url')
def get_info():
    f = open('secret_token', 'w')
    f.close()
    g = open('secret_session', 'w')
    g.close()
    return template('url_form')

#user tweets work
@post('/translated')
def serve_translation():
    new_string = new_translation()
    user_name = ''
    json_tweets = None
    if os.path.isfile('./secret_session') and os.path.getsize('./secret_session') == 0:
        user_auth()
    if os.path.isfile('./secret_session') and os.path.getsize('./secret_session') > 0:
        oauth_session = access_secrets('secret_session')
        #user_tweet(oauth_session, new_string)
        user_dict = access_secrets('secret_token')
        user_name = user_dict['screen_name']
        tweets = user_timeline(oauth_session, user_name)
        json_tweets = tweets.json()
    else:
        #preteenify_tweet(new_string) #totally hates duplicate statuses
        user_name = 'PRETEENIFY' #mildly unnecessary
    return template('translated', new_string=new_string, user_name=user_name, tweets=json_tweets)  

def new_translation():
    word_string = request.forms.get('word_string')
    new_string = translate(word_string)
    save_string(new_string)
    return new_string

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
        'more' : 'moar',
        'though' : 'tho',
        'school' : 'skool',
        's' : '$',
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

#logging out works
@route('/signed-out')
def sign_out():
    if os.path.isfile('./secret_session'):
        os.remove('./secret_session')
    if os.path.isfile('./secret_token'):
        os.remove('./secret_token')
    return serve_index() #returns home page 

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
