from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app) #Die Flask API

api_content = []

class SimpleClass(Resource):
     def get(self):
        return api_content


class SimpleNameScore(Resource):
    def get(self, name):
        if name in api_content:
            return {name: api_content[name]}
        return {"Message" : "Nicht vorhanden"}

    def put(self, name, key):
        for n in api_content:
            print(n)
            if n[0] == str(name) and n[1] == str(key):
                api_content.remove(n)
        ansArr = [request.form['name'], request.form['symbole'], request.form['cnt']]
        api_content.append(ansArr)
        return {"Message": "Neu hinzugefügt"}


#Hier passiert das Mapping auf die Klasse
api.add_resource(SimpleClass, '/')
api.add_resource(SimpleNameScore, '/upload/<string:name>/<string:key>')

if __name__ == '__main__':
    app.run(debug=True) #debug=True lädt nach den Änderungen neu
