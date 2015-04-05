#!flask/bin/python

from newGraph import *
from flask import *
import os

SharedMem = ""
title = "RU Jarvis - AI Navigation System"
app = Flask("app")
stops = json.load(open('Data/stops.ap.json'))

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title=title,stops=stops)

@app.route('/about')
def abt():
    return render_template("about.html", title=title+" [About]")

@app.route('/images/<path:sprite>')
def images(sprite):
    return send_from_directory(os.path.join(app.static_folder,"images"),sprite)

@app.route('/js/<path:script>')
def js(script):
    return send_from_directory(os.path.join(app.static_folder,"js"),script)

@app.route('/css/<path:style>')
def css(style):
    return send_from_directory(os.path.join(app.static_folder,"css"),style)

@app.route('/favicon.ico')
def iconload():
    return send_from_directory(app.static_folder,'icon.jpg', mimetype='image/vnd.microsoft.icon')

@app.route('/solve',methods=['POST'])
def conv():
    return str(get_best_path(request.form['start'], request.form['dest']))

@app.route('/query/<path:query>')
def route(query):
    return render_template("query.html",query=query,title=title+" [Query]",makeDiGraph=makeDiGraph,isExisting=isExisting,closest_stops=closest_stops)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
