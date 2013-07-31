import os, psycopg2, urlparse
from local_settings import DATABASE_KEY

from bottle import route, run, template, get, post, request, static_file, error

def connecting():
    urlparse.uses_netloc.append("postgres")
    DATABASE_URL = DATABASE_KEY
    try:
        url = urlparse.urlparse(os.environ["DATABASE_URL"])
    except KeyError:
        url = urlparse.urlparse(DATABASE_URL)
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

@route('/')
def serve_index():
    return static_file('index.html', root='static/')

@post('/translated')
def serve_translation():
    word_string = request.forms.get('word_string')
    new_string = translate(word_string)
    save_string(new_string)
    return '''<link rel=stylesheet type=text/css href="static/style.css">
	      <body>
    	        <h1 align = "center">
      		  <a href="/">PRETEENIFY</a>
    		</h1>
    		<div class="words">
		'''+ new_string +'''</div>
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
    

def translate(word_string):

    vocab_dict = {
        'to' : '2',
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
    return 'YOU BROKE THE WEBSITE BRO'

@error(500)
def error500(error):
    word_string = request.forms.get('word_string')
    return 'SOMETHING TERRIBLE HAPPENED: HERE\'S YOUR TRANSLATION ' + translate(word_string)

run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
#heroku setting

#run(host='localhost', port=8080, debug=True)
#local dev setting
