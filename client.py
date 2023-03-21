import requests


data = requests.post('http://127.0.0.1:5000/users/', json={'username': 'Garry Potter', 'password': 'Gar_12_pot'})
print(data.status_code)
print(data.json())

data = requests.get('http://127.0.0.1:5000/users/')
print(data.status_code)
print(data.json())

data = requests.patch('http://127.0.0.1:5000/users/1', json={'username': 'Garry'})
print(data.status_code)
print(data.json())

data = requests.delete('http://127.0.0.1:5000/users/1')
print(data.status_code)
print(data.json())
