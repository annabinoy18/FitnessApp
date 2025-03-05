from pymongo import MongoClient

MONGO_URI = "mongodb+srv://annoy18:annabinoy18@cluster0.nqvvl.mongodb.net/FITNESSAPPDB?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "FITNESSAPPDB"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collection Names
WORKOUTS_COLLECTION = "workouts"
WORKOUT_TODAY_COLLECTION = "workout_today"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Get Collections
workouts_collection = db[WORKOUTS_COLLECTION]
workout_today_collection = db[WORKOUT_TODAY_COLLECTION]



def insert_workout(workout_data):
    """Insert a new workout into the database."""
    workouts_collection.insert_one(workout_data)


def delete_workout(video_id):
    """Delete a workout from the database using its video ID."""
    workouts_collection.delete_one({"video_id": video_id})


def get_all_workouts():
    """Retrieve all workouts from the database."""
    return list(workouts_collection.find({}, {"_id": 0, "video_id": 1, "channel": 1, "title": 1, "duration": 1}))


def get_workout_today():
    """Get today's workout from the database."""
    return list(workout_today_collection.find({"id": 0}, {"_id": 0}))


def update_workout_today(workout_data, insert=False):
    """Update or insert today's workout."""
    workout_data["id"] = 0
    if insert:
        workout_today_collection.insert_one(workout_data)
    else:
        workout_today_collection.update_one({"id": 0}, {"$set": workout_data}, upsert=True)