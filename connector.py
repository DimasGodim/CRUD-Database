import mysql.connector
from pymongo import MongoClient

def SQL():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="nft"
    )
    return db

def MONGGO():
    client_ip = MongoClient("mongodb://localhost:27017/")
    db = client_ip["NFT"]
    file = db["asset"]
    return file
