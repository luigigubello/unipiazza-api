# Unipiazza Python API 

![](https://img.shields.io/badge/release-v1.0.0-blue.svg) ![](https://img.shields.io/badge/Python-3.5%7C3.6%7C3.7-blue.svg) ![](https://img.shields.io/badge/Unipiazza-%E2%9D%A4%EF%B8%8F%20Python-blue.svg)

Introduction
=========

This module provides a Python interface for the [Unipiazza API](https://unipiazza-api.herokuapp.com/docs/v1/ "Unipiazza API"). It works with Python 3. Made with ❤️.

How to use
=========

Install the requirements:

```sh
sudo pip install requests
```

Generate your own **refresh token**:

```sh
curl "http://unipiazza-api.herokuapp.com/auth/sign_in" -d "email=your@email.com" -d "password=your_secret"
```

Import Unipiazza module in Python and set the refresh token:

```python
import unipiazza
refresh_token = 'YOUR_SUPER_SECRET_REFRESH_TOKEN'
tokens = unipiazza.token(refresh_token)
```

Functions
------

### .token

Using the user's refresh_token, the function **token** generates a *token* and a **new** *refresh token*. The function returns a *token*, a new *refresh token* and the *user ID*.

* **Input:** the refresh token
* **Output:** a dictionary where the keys are *token*, *refresh_token* and *user_id*

##### Example

```
>>> tokens = unipiazza.token(refresh_token)
>>> print(tokens)
{"token": 'value', "refresh_token": 'value', "used_id": 'value'}
```

### .user_info

Using your own *token* and the *ID* of **any** user, this function returns a dictionary with some user's information.

* **Input:** the token and an user ID
* **Output:** a dictionary with these keys: *user_id*, *first_name*, *last_name*, *gender*, *birthday*, *unipoint*, *status*, *has_pass*, *visited_shops_counter*, *receipts_counter*,*prizes_counter* and *friends_counter*. If the user ID is own there is also the key *email*

##### Example

```python
my_account = unipiazza.user_info(tokens['token'], tokens['user_id'])
if my_account != None:
	print("""
Informazioni account\n
	Nome: {}
	Cognome: {}
	Unipoint: {}
	Livello: {}
	Checkin: {}
	Premi: {}
""".format(my_account['first_name'], my_account['last_name'], my_account['unipoint'], my_account['status'], my_account['receipts_counter'], my_account['prizes_counter']))
```

### .shop_info

Using your own *token* and the *ID* of **any** shop, this function returns a dictionary with some shop's information.

* **Input:** the token and an user ID
* **Output:** a dictionary with these keys: *shop_id*, *name*, *description*, *category*, *phone*, *email*, *address*, *latitude*, *longitude* and *website*

### .user_list

This function returns a list of user IDs. The input values are the *token*, the *number* of the user IDs to be extracted and the *number* of users [per page](https://unipiazza-api.herokuapp.com/docs/v1/#index "per page").

* **Input:** the token, the length of the returned list and the number of users per page.
* **Output:** a list of user IDs

### .shop_list

This function returns a list of shop IDs. The input values are the *token*, the *number* of the shop IDs to be extracted and the *number* of shops per page.

* **Input:** the token, the length of the returned list and the number of shops per page.
* **Output:** a list of shop IDs

### .friends

Using your own *token* and the *ID* of **any** user, this function returns a list of dictionaries with the information of the user's friends.

* **Input:** the token and an user ID
* **Output:** a list of dictionaries with these keys for each user's friend: *user_id*, *first_name*, *last_name*, *gender*, *birthday*, *unipoint*, *status*, *has_pass*, *visited_shops_counter*, *receipts_counter*,*prizes_counter* and *friends_counter*

##### Example

```python
my_friends = unipiazza.friends(tokens['token'], tokens['user_id'])
if my_friends != None and my_friends != []:
	print("Lista amici")
	for item in my_friends:
		print("""
	Nome: {}
	Cognome: {}
""".format(item['first_name'], item['last_name']))
```

### .history

Using your own *token* and your *ID* or the *ID* of **any** own friend, this function returns a list of dictionaries with the information about each user's [receipts](https://unipiazza-api.herokuapp.com/docs/v1/#history "receipts").

* **Input:** the token and an user ID
* **Output:** a list of dictionaries with these keys for each one: *history_id*, *user_id*, *shop_id*, *shop_name*, *shop_address*, *shop_latitude*, *shop_longitude*, *created_at*, *likes_counter*, *comments_counter*, *receipt_id* and *coins*

##### Example

```python
my_history = unipiazza.history(tokens['token'], tokens['user_id'])
if my_history != None and my_history != []:
	print("Ricevute")
	for item in my_history:
		print("""
	ID: {}
	Monete: {}
	Negozio: {}
	Like: {}
	Commenti: {}
""".format(item['receipt_id'], item['coins'], item['shop_name'], item['likes_counter'], item['comments_counter']))
```

### .visited_shops

Using your own *token* and the *ID* of **any** user, this function returns a list of dictionaries with the information about the shops where the user have done a check-in.

* **Input:** the token and an user ID
* **Output:** a list of dictionaries with these keys for each one: *shop_id*, *name*, *description*, *city*, *address*, *website*, *facebook*, *receipts_counter* and *coins*

##### Example

```python
my_shops = unipiazza.visited_shops(tokens['token'], tokens['user_id'])
if my_shops != None and my_shops != []:
	print("Negozi visitati")
	for item in my_shops:
		print("""
	Nome: {}
	Città: {}
	Checkin: {}
	Monete: {}
	Facebook: {}
""".format(item['name'], item['city'], item['receipts_counter'], item['coins'], item['facebook']))
	print("\nMaggiori informazioni sui negozi visitati")
	for item in my_shops:
		shop_info = unipiazza.shop_info(tokens['token'], item['shop_id'])
		if shop_info != None:
			print("""
		ID: {}
		Nome: {}
		Descrizione: {}
		Tipo: {}
		Telefono: {}
		Email: {}
		Indirizzo: {}
		Latitudine: {}
		Longitudine: {}
		Website: {}
	""".format(shop_info['shop_id'], shop_info['name'], shop_info['description'], shop_info['category'], shop_info['phone'], shop_info['email'], shop_info['address'], shop_info['latitude'], shop_info['longitude'], shop_info['website']))
```






