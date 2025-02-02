# Package Imports
from multiprocessing import connection
from pymongo import MongoClient
from bson import Timestamp, ObjectId
from fnHelper import jsonIO
from fnHelper.cryptography.aes256_encryption import *

class Database:
    def __init__(self):
        try:
            connection_string = decrypt(jsonIO.read_items('config.json')['uri'], "AUP52623BSIT")
            self.client = MongoClient(connection_string)
            self.database = self.client['aupaydb']

            self.collection = {
                'users': self.database['users'],
                'transactions': self.database['transactions']
            }

            try:
                if not self.client.list_database_names().__contains__('aupaydb'):
                    self.__create_database()
            except Exception as e:
                print(f"Error: \n{e}")
        except:
            print("Configure URI in config.json")

    # Initial collection documents
    def __create_database(self):
        coinbase = ObjectId('ffffffffffffffffffffffff')
        self.database.create_collection('users', validator=user_schema)
        self.database.create_collection('transactions', validator=transaction_schema)
        initial_user = {
            'card_id': "7f453b1936a11e152d5cd96c66cdd4caf13024c390509f71daf5410c1d742986",
            'school_id': "AUP52623BSIT",
            'password': "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
            'secret_key': "AUP52623BSITAUP52623BSITAUP52623",
            'user_type': 'admin',
            'max_credit': float(0.00),
            'balance': float(0.00),
        }
        user = self.collection['users'].insert_one(initial_user)

        # initial_transaction = {
        #     'timestamp': Timestamp(1685084400, 0),
        #     'source_id': coinbase,
        #     'destination_id': user.inserted_id,
        #     'amount': float(0.00),
        #     'description': "Coinbase transaction",
        # }
        # transaction = self.collection['transactions'].insert_one(initial_transaction)

        print("Initial database created.")

user_schema = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['_id', 'card_id', 'school_id', 'password', 'secret_key', 'user_type'],
        'properties': {
            '_id': {
                'bsonType': 'objectId'
            },
            'card_id': {
                'bsonType': 'string',
                'pattern': '^[a-fA-F0-9]{64}$'
            },
            'school_id': {
                'bsonType': 'string',
            },
            'password': {
                'bsonType': 'string',
                'pattern': '^[a-fA-F0-9]{64}$'
            },
            'secret_key': {
                'bsonType': 'string',
                # 'pattern': '^[A-Z2-7]+=*$'
            },
            'user_type': {
                'enum': ['admin', 'user', 'business', 'teller']
            },
            'max_credit': {
                'bsonType': 'double',
            },
            'balance': {
                'bsonType': 'double',
            }
        }
    }
}

transaction_schema = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['timestamp', 'source_id', 'destination_id', 'amount', 'description'],
        'properties': {
            'timestamp': {
                # 'bsonType': 'int'
            },
            'source_id': {
                'bsonType': 'objectId'
            },
            'destination_id': {
                'bsonType': 'objectId'
            },
            'amount': {
                'bsonType': 'double',
                'minimum': 1
            },
            'description': {
                'bsonType': 'string',
                'minLength': 1
            }
        }
    }
}
