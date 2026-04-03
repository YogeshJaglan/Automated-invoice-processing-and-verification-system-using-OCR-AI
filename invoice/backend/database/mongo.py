from pymongo import MongoClient

# MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://gullykart:8920123828@cluster0.3szn5oe.mongodb.net/?retryWrites=true&w=majority"

# Create client
client = MongoClient(MONGO_URI)

# Select database
db = client["invoice_db"]

# Select collection
invoices_collection = db["invoices"]