from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import sqlite3

class CryptoManager():
	"""Backend of the Kryp-Toes application to manage the cryptocurrency porfolio
	and connect to an online server for the most up-to-date information."""

	def __init__(self):
		"""Instantiate the manager object. Connect to the server and SQL database."""

		# Create and initialize data members to connect to server
		self._api_key = None
		self._url = None
		self._header = None
		self._session = None
		self.connect_server()

		# Data member for database connection
		self._database_connection = None
		self.connect_database()

	def connect_server(self):
		"""Connect to the server for the most up-to-date information."""

		# Get the API key from a file
		with open('API_key.txt', 'r') as reader:
			self._api_key = reader.read()
		reader.close()

		# Connect to the server (coinmarketcap.com)
		self._url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
		self._header = {
			"Accepts": "application/json",
			"X-CMC_PRO_API_KEY": self._api_key,
		}
		self._session = Session()
		self._session.headers.update(self._header)

	def connect_database(self):
		"""
		Connect to database

		:return: a tuple containing the connection
		"""
		# TO DO

		# If database does not already exists, create one.
		# table for user data: user_id, username (string), hashed_password (string), cash_amount (float)


		# Connect to the database
		self._database_connection = sqlite3.connect("Kryptoes.db")
		cursor = self._database_connection.cursor()

		# create table for portfolio if it does not already exist
		cursor.execute("""CREATE TABLE IF NOT EXISTS portfolio (
						crypto_name text,
						crypto_id int,
						quantity float,
						price float
						)""")

		"""
		# create table that keeps track of the cryptocurrencies user has
		cursor.execute(CREATE TABLE IF NOT EXISTS cryptocurrencies (
				        crypto_name text
				        ))
		"""

		self._database_connection.commit()

	def add_to_portfolio(self, crypto_name, crypto_id, quantity, price):
		"""
		Adds a cryptocurrency to user's portfolio
		"""

		# Connect to database
		connection = self._database_connection
		cursor = connection.cursor()

		# append purchase to portfolio
		cursor.execute("INSERT INTO portfolio VALUES (:crypto_name, :crypto_id, :quantity, :price)",
					{
						"crypto_name": crypto_name,
						"crypto_id": crypto_id,
						"quantity": quantity,
						"price": price
					})

		"""
		# retrieve all cryptocurrencies user holds
		cursor.execute("SELECT crypto_name FROM cryptocurrencies")

		# list of all cryptocurrencies
		crypto_list = [name[0] for name in cursor.fetchall()]

		# if new crypto, add to user's list of cryptocurrencies
		if crypto_name not in crypto_list:
			cursor.execute("INSERT INTO cryptocurrencies VALUES (:crypto_name)",
							{
								"crypto_name": crypto_name
							})
		"""

		connection.commit()

		# connection.close()

	"""
	def get_total_cryptocurrencies(self):
		
		# Returns the total distinct cryptocurrencies user has in portfolio
	

		# connect to database
		connection = self._database_connection
		cursor = connection.cursor()

		# retrieve number of cryptocurrencies
		cursor.execute("SELECT COUNT() FROM wallet")
		total_crypto = cursor.fetchall()

		# returns the number of cryptocurrencies user has
		return total_crypto[0]
	"""

	def get_quantity(self, crypto_name):
		pass

	def get_price(self):
		pass


	def create_account(self, username, password, cash_amount):
		"""Create an user account."""
		#BONUS
		pass

	def hash_password(self, password):
		"""Encrypt the password."""
		#BONUS
		pass

	def authenticate(self, username, hashed_password):
		"""Take username and password as parameter and authenticate the current user."""
		#BONUS
		pass

	def lookup_id(self, cryto_name):
		"""Take the name of the cryptocurrency as parameter and
		return the id of the currency according to coinmarketcap.com"""
		# TO DO
		pass

	def get_current_price(self, cryto_id):
		"""Take the id of the cryptocurrency as parameter.
		Query and return the most up-to-date price of that cryptocurrency."""

		# Parameters for Query
		parameters = {
			"start": cryto_id,
			"limit": "1",
			"convert": "USD"
		}

		# Pull cryptocurrency data from the server
		try:
			response = self._session.get(self._url, params=parameters)
			data = json.loads(response.text)
			return data["data"][0]["quote"]["USD"]["price"]

		# Handle all connection errors
		except (ConnectionError, Timeout, TooManyRedirects) as error_message:
			print(error_message)

		# TO DO


	def buy_crypto(self, user_id, cryto_id, units):
		"""Take the user id, cryptocurrency id, and units to invest as parameters and make the purchase."""
		# TO DO

		# Ensure the user has enough cash on hand

		# Make the purchase
		#   decrease the cash_amount
		#   query the current price of the cryptocurrency
		#   update the holding for the cryptocurrency
		#       make a new entry for every purchase? (to keep track of net gain/loss)
		pass

	def sell_crypto(self, user_id, cryto_id, units):
		"""Take the user id, cryptocurrency id, and units to be sold as parameters and make the sell."""
		# TO DO

		# Ensure the user has this cryptocurrency in porfolio
		# Ensure the user has enough units on hand to be sold

		# Make the sell
		#   decrease or delete the holding
		#   query the current price of the cryptocurrency
		#   increase the cash amount
		pass
