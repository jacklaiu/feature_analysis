# -*- coding: gbk -*-
from flask import Flask, abort, request, jsonify
import analysis.concept.Common as ay_com
app = Flask(__name__, static_url_path='')
app.config['JSON_AS_ASCII'] = False

#Opt______________________________________________________________________________________________________________________________________________

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/get_zhangting_concepts/<dayCount>')
def get_zhangting_concepts(dayCount):
    map = ay_com.get_zhangtingconcept_countMap(dayCount)
    return jsonify(map)

#WebView__________________________________________________________________________________________________________________________________________

@app.route('/html/get_zhangting_concepts/')
def view_get_zhangting_concepts():
    return app.send_static_file('html/get_zhangting_concepts.html')#homepage.html在static文件夹下

if __name__ == '__main__':
    app.run()