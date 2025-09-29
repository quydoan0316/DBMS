from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

MONGO_DETAILS = "mongodb://localhost:27017/"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client["DBMS"]

# Tạo bucket GridFS async
fs_bucket = AsyncIOMotorGridFSBucket(database)

# Collection lưu thông tin file (metadata, filename, file_id, ...)
files_collection = database["fs.files"]
chunks_collection = database["fs.chunks"]
patients_diagnosis = database["patients.diagnosis"]
patients_medicalHistory = database["patients.medicalHistory"]






