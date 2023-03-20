import requests


data = requests.post('http://127.0.0.1:5000/users/', json={'username': 'Garry Potter', 'password': 'Gar_12_pot'})
print(data.status_code)
print(data.json())

