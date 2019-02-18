import os, psycopg2, urlparse, tweetpony, requests_oauthlib, pickle 

from requests_oauthlib import OAuth1Session

from bottle import route, run, template, get, post, request, static_file, error, redirect

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]

O_ID = None
RESPONSE = None

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

def edit_db(command, *args):
    connection = connecting()
    cur = connection.cursor()
    param_dict = {}
    o_id = None
    count = 1
    for data in args:
       param_dict['key'+ str(count)] = data
       count += 1
    if "RETURNING" in command:
        cur.execute(command, param_dict)
        tup = cur.fetchone()
        o_id = tup[0]
    else:
        cur.execute(command, param_dict)
    connection.commit()
    cur.close()
    connection.close()
    return o_id

def access_info(command, o_id):
    connection = connecting()
    cur = connection.cursor()
    cur.execute(command, {'key' : o_id})
    tup = cur.fetchone()
    data = tup[0]
    cur.close()
    connection.close()
    return data

def preteenify_tweet(string):
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
    api = tweetpony.API(
        consumer_key=CONSUMER_KEY, 
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    api.update_status(status = string) #just now realized i was using a keyword...

def auth_url(CONSUMER_KEY, CONSUMER_SECRET):
    api = tweetpony.API(CONSUMER_KEY, CONSUMER_SECRET)
    auth_url = api.get_auth_url()
    return auth_url #sign in with twitter button url

def user_auth():
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    authentication_url = 'https://api.twitter.com/oauth/authenticate'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth_session = OAuth1Session(
        client_key=CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        callback_uri='http://preteenify.herokuapp.com/get-url'
        #callback_uri='http://0.0.0.0:5000/get-url'
    )
    #first step
    oauth_session.fetch_request_token(request_token_url)
    #second step
    oauth_session.authorization_url(authentication_url)
    #third step
    global RESPONSE
    oauth_session.parse_authorization_response(RESPONSE)
    token = oauth_session.fetch_access_token(access_token_url) #this is dict!
    oauth_str = pickle.dumps(oauth_session)
    token_str = pickle.dumps(token)
    command = "INSERT INTO oauth_tokens (session, token) VALUES (%(key1)s, %(key2)s) RETURNING o_id"
    o_id = edit_db(command, oauth_str, token_str)
    return o_id

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
    global O_ID
    o_id = O_ID
    url =  auth_url(CONSUMER_KEY, CONSUMER_SECRET)
    return template('index', url=url, O_ID=o_id)
    
#HAI NO MORE COPY/PASTE URLS == USER SO HAPPY!
@route('/get-url')
def get_info():
    global RESPONSE
    RESPONSE = request.url #requesting current url!!
    return template('url_form')

#PRETEENIFY TWEETS
@post('/translated')
def serve_translation():
    new_string = new_translation()
    preteenify_tweet(new_string) #totally hates duplicate statuses
    url = auth_url(CONSUMER_KEY, CONSUMER_SECRET)
    return template('translated', new_string=new_string, url=url)  

#USER TWEETS
@post('/translated_user')
def serve_translation():
    new_string = new_translation()
    user_name = ''
    json_tweets = None
    global O_ID
    global RESPONSE
    if RESPONSE:
        O_ID = user_auth()
    if O_ID:
        command = "SELECT session FROM oauth_tokens WHERE o_id = (%(key)s)"
        oauth_session = pickle.loads(access_info(command, O_ID)) #unpickle it
        user_tweet(oauth_session, new_string)
        command = "SELECT token FROM oauth_tokens WHERE o_id = (%(key)s)"
        user_dict = pickle.loads(access_info(command, O_ID)) #unpickle it
        user_name = user_dict['screen_name']
        tweets = user_timeline(oauth_session, user_name)
        json_tweets = tweets.json()
    return template('translated_user', new_string=new_string, user_name=user_name, tweets=json_tweets)

def new_translation():
    word_string = request.forms.get('word_string')
    new_string = translate(word_string)
    command = "INSERT INTO preteenify VALUES (%(key1)s)"
    edit_db(command, new_string)
    return new_string

def load_dict():
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
        'boy' : 'boi',
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
        'baby': 'bb',
    }
    return vocab_dict

def translate(word_string):

    vocab_dict = load_dict() 

    for key in vocab_dict:
        if key in word_string:
	    word_string = word_string.replace(key, vocab_dict[key])

    words = word_string.split(" ")
    index = 0

    for each in words:
        length = len(each)
        each = each.lower()
        for i in range(0, length):
	    if i % 2 == 0:
                if each[i] == 'i':
                    if i != 0: #don't want negative indexing
                        each = each.replace(each[i-1], each[i-1].upper())
                        continue #the people have spoken & want better readability
	        each = each.replace(each[i], each[i].upper())
        words[index] = each
	index+=1
    return '((~* ' + ' '.join(words) + ' *~))'

#logging out works
@route('/signed-out')
def sign_out():
    global O_ID
    command = "DELETE FROM oauth_tokens WHERE o_id = (%(key1)s)"
    edit_db(command, O_ID)
    O_ID = None
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
                  <p>''' + translate(word_string) + '''</p>
		</div>
                <div class="lindsay">
                  <img src="static/lindsay_palm.gif">
                </div>
              </body> '''

run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
#heroku setting

#run(host='localhost', port=8080, debug=True)
#local dev setting
