import requests
import json

host = 'http://localhost:5000/upload'
response = requests.put('%s/%s' % (host, 'Fub'), data={'name' : 'Fub', 'symbole' : 'rock' , 'cnt' : 10})

print(response)
