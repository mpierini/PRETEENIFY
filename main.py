import os
from bottle import route, run, template, get, post, request, static_file, error


@route('/')
def serve_index():
    return static_file('index.html', root='static/')

@post('/translated')
def serve_translation():
    word_string = request.forms.get('word_string')
    new_string = translate(word_string)
    return '''<link rel=stylesheet type=text/css href="static/style.css">
	      <body>
    	        <h1 align = "center">
      		  <a href="/">PRETEENIFY</a>
    		</h1>
    		<div class="words">
		((~* '''+ new_string +''' *~))</div>
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
	'night' : 'nite',
	'girl' : 'gurl',
	'and' : '&',
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
    return ' '.join(words)


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

run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
#heroku setting

#run(host='localhost', port=8080, debug=True)
#local dev setting
