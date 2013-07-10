from bottle import route, run, template, get, post, request, static_file, error

#okay now i want to make the translation area better for longer ones

@route('/')
def serve_index():
    return static_file('index.html', root='static/')

@post('/translated')
def translate():
    word_string = request.forms.get('word_string')
    new_string = weirdCaps(word_string)
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
    
def weirdCaps(word_string):
    words = word_string.split(" ")
    count = 0
    index = 0
    for each in words:
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
#def get_animated():
#    return '/static/favicon.ico'

def serve_favicon():
    return static_file('favicon.ico', root='static/')
    #only works for static icon

@error(404)
def error404(error):
    return 'YOU BROKE THE WEBSITE BRO'

#run(host='localhost', port=8080, debug=True)
#potentially needed to comment out this port #
