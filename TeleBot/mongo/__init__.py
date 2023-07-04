import config
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

mongo = MongoClient(config.MONGO_DB_URL)
db = mongo.TeleBot