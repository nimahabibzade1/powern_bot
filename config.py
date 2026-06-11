import os


database_config = {'user': os.environ.get('database_user'), 'password': os.environ.get('database_password'), 'host': os.environ.get('database_host')}

database_name = os.environ.get('database')

API_TOKEN = os.environ.get('API_TOKEN')
