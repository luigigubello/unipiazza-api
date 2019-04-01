# Unipiazza API V1
# Python 3.7
# https://realpython.com/api-integration-in-python/

import requests

# Ritorna dizionario con Token e Refresh Token
def token(refresh_token):
	endpoint = 'https://unipiazza-api.herokuapp.com/auth/refresh_token'
	data = {'refresh_token' : refresh_token}
	resp = requests.post(endpoint, data=data).json()
	if resp['error'] == True:
		print("Error: {}".format(resp['msg']))
		return None
	else:
		return {
			'token':resp['token'], 
			'refresh_token':resp['refresh_token'],
			'user_id':resp['user']['id']
			}

# Ritorna dizionario con alcune informazioni relative all'utente
def user_info(token, user_id):
	endpoint = 'http://unipiazza-api.herokuapp.com/api/v1/users/' + user_id
	headers = {'Authorization': 'Bearer ' + token}
	resp = requests.get(endpoint, headers=headers).json()
	if 'error' in resp:
		if 'msg' in resp:
			print("Error: {}".format(resp['msg']))
		else:
			print("Error: {}".format(resp))
		return None			
	else:
		account_info = {
			'user_id':resp['id'],
			'first_name':resp['first_name'],
			'last_name':resp['last_name'],
			'gender':None,
			'birthday':None,
			'unipoint':resp['unipoint'],
			'status':resp['status'],
			'has_pass':resp['has_pass'],
			'visited_shops_counter':resp['visited_shops_counter'],
			'receipts_counter':resp['receipts_counter'],
			'prizes_counter':resp['prizes_counter'],
			'friends_counter':resp['friends_counter']
			}
		if 'gender' in resp:
			account_info.update({'gender':resp['gender']})
		if 'birthday' in resp:
			account_info.update({'birthday':resp['birthday']})
		if 'email' not in resp:	# Dati di altri utenti
			return account_info
		else:	# Dati del proprio utente
			account_info['email'] = resp['email']
			return account_info

# Ritorna dizionario con alcune informazioni relative al negozio
def shop_info(token, shop_id):
	endpoint = 'http://unipiazza-api.herokuapp.com/api/v1/shops/' + shop_id
	headers = {'Authorization': 'Bearer ' + token}
	resp = requests.get(endpoint, headers=headers).json()
	if 'error' in resp:
		if 'msg' in resp:
			print("Error: {}".format(resp['msg']))
		else:
			print("Error: {}".format(resp))
		return None			
	else:
		shop_info = {
			'shop_id':resp['id'],
			'name':resp['name'],
			'description':None,
			'category':resp['category'],
			'phone':None,
			'email':None,
			'address':None,
			'latitude':None,
			'longitude':None,
			'website':None
			}
		if 'description' in resp:
			shop_info.update({'description':resp['description']})
		if 'phone' in resp:
			shop_info.update({'phone':resp['phone']})
		if 'email' in resp:
			shop_info.update({'email':resp['email']})
		if 'address' in resp:
			shop_info.update({'address':resp['address']})
		if 'latitude' in resp:
			shop_info.update({'latitude':resp['latitude']})
		if 'longitude' in resp:
			shop_info.update({'longitude':resp['longitude']})
		if 'website' in resp['links']:
			shop_info.update({'website':resp['links']['website']})
		return shop_info

# Ritorna una lista di utenti
def user_list(token, number, per_page):
	user_ids = []
	i = 0
	j = 0
	headers = {'Authorization': 'Bearer ' + token}
	while i < number:
		endpoint = 'http://unipiazza-api.herokuapp.com/api/v1/users?page=' + str(j) + '&per_page=' + str(per_page)
		resp = requests.get(endpoint, headers=headers).json()
		if len(resp) == 0:
			break
		for item in resp:
			user_ids.append(item['id'])
		i = i + len(resp)
		j += 1
	return user_ids

# Ritorna una lista di negozi
def shop_list(token, number, per_page):
	shop_ids = []
	i = 0
	j = 0
	headers = {'Authorization': 'Bearer ' + token}
	while i < number:
		endpoint = 'http://unipiazza-api.herokuapp.com/api/v1/shops?page=' + str(j) + '&per_page=' + str(per_page)
		resp = requests.get(endpoint, headers=headers).json()
		if len(resp) == 0:
			break
		for item in resp:
			shop_ids.append(item['id'])
		i = i + len(resp)
		j += 1
	return shop_ids

# Ritorna lista di dizionari con informazioni sugli amici dell'utente
def friends(token, user_id):
	endpoint = 'http://unipiazza-api.herokuapp.com/api/v1/users/' + user_id + '/friends'
	headers = {'Authorization': 'Bearer ' + token}
	resp = requests.get(endpoint, headers=headers).json()
	if 'error' in resp:
		if 'msg' in resp:
			print("Error: {}".format(resp['msg']))
		else:
			print("Error: {}".format(resp))
		return None	
	else:
		resp = resp['friends']
		if resp == []:
			return []
		else:
			friends = []
			for item in resp:
				element = {
					'user_id':item['id'],
					'first_name':item['first_name'],
					'last_name':item['last_name'],
					'gender':None,
					'birthday':None,
					'unipoint':item['unipoint'],
					'status':item['status'],
					'has_pass':item['has_pass'],
					'visited_shops_counter':item['visited_shops_counter'],
					'receipts_counter':item['receipts_counter'],
					'prizes_counter':item['prizes_counter'],
					'friends_counter':item['friends_counter']
					}
				if 'gender' in item:
					element.update({'gender':item['gender']})
				if 'birthday' in item:
					element.update({'birthday':item['birthday']})
				friends.append(element)
		return friends

# Ritorna una lista di dizionari contenente la storia di un utente
def history(token, user_id):
	i = 0
	endpoint = 'http://unipiazza-api.herokuapp.com/api/v1/users/' + user_id + '/history?page=' + str(i) + '&per_page=50'
	headers = {'Authorization': 'Bearer ' + token}
	resp = requests.get(endpoint, headers=headers).json()
	if 'error' in resp:
		if 'msg' in resp:
			print("Error: {}".format(resp['msg']))
		else:
			print("Error: {}".format(resp))
		return None
	else:
		resp = resp['history']
		if resp == []:
			return []
		else:
			history = []
			while resp != []:
				for item in resp:
					if item['type'] == 'receipt':	# Per ora fornisce info acquisti
						element = {
							'history_id':item['id'],
							'user_id':item['user']['id'],
							'shop_id':item['shop']['id'],
							'shop_name':None,
							'shop_address':None,
							'shop_latitude':None,
							'shop_longitude':None,
							'created_at':item['created_at'],
							'likes_counter':item['likes_counter'],
							'comments_counter':item['comments_counter'],
							'receipt_id':item['receipt']['id'],
							'coins':None,
							}
						if 'name' in item['shop']:
							element.update({'shop_name':item['shop']['name']})
						if 'address' in item['shop']:
							element.update({'shop_address':item['shop']['address']})
						if 'latitude' in item['shop']:
							element.update({'shop_latitude':item['shop']['latitude']})
						if 'longitude' in item['shop']:
							element.update({'shop_longitude':item['shop']['longitude']})
						if 'coins' in item['receipt']:
							element.update({'coins':item['receipt']['coins']})
						history.append(element)
					
				i += 1
				endpoint = 'http://unipiazza-api.herokuapp.com/api/v1/users/' + user_id + '/history?page=' + str(i) + '&per_page=50'
				resp = requests.get(endpoint, headers=headers).json()
				resp = resp['history']
			return history

# Ritorna lista di dizionari con alcune informazioni sui negozi frequentati dall'utente
def visited_shops(token, user_id):
	endpoint = 'http://unipiazza-api.herokuapp.com/api/v1/users/' + user_id + '/visited_shops'
	headers = {'Authorization': 'Bearer ' + token}
	resp = requests.get(endpoint, headers=headers).json()
	if 'error' in resp:
		if 'msg' in resp:
			print("Error: {}".format(resp['msg']))
		else:
			print("Error: {}".format(resp))
		return None
	else:
		resp = resp['shops']
		if resp == []:
			return []
		else:
			shops = []
			for item in resp:
				if item['receipts_counter'] != 0:	# Solo quelli dove è stato effettuato un checkin
					element = {
						'shop_id':item['id'],
						'name':item['name'],
						'description':None,
						'city':None,
						'address':None,
						'website':None,
						'facebook':None,
						'receipts_counter':item['receipts_counter'],
						'coins':item['coins']
						}
					if 'description' in item:
						element.update({'description':item['description']})
					if 'city' in item:
						element.update({'city':item['city']})
					if 'address' in item:
						element.update({'address':item['address']})
					if 'website' in item['links']:
						element.update({'website':item['links']['website']})
					if 'facebook' in item['links']:
						element.update({'facebook':item['links']['facebook']})
					shops.append(element)
			return shops
