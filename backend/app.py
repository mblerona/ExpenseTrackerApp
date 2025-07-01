
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from datetime import datetime
from bson import ObjectId
import os

# app = Flask(__name__)
# CORS(app)

# app.config["MONGO_URI"] = "mongodb://mongo:27017/expenses"
# mongo = PyMongo(app)

user = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")
host = os.getenv("MONGO_HOST", "mongo")
port = os.getenv("MONGO_PORT", "27017")
db = os.getenv("MONGO_DB", "expenses")

app.config["MONGO_URI"] = f"mongodb://{user}:{password}@{host}:{port}/{db}"



@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()
    try:
        amount = float(data.get("amount"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid amount"}), 400

    expense = {
        "amount": amount,
        "category": data.get("category"),
        "date": data.get("date") or datetime.utcnow().isoformat()
    }
    mongo.db.records.insert_one(expense)
    return jsonify({"msg": "Expense added!"}), 201

@app.route("/expenses", methods=["GET"])
def get_expenses():
    expenses = mongo.db.records.find()
    result = [{
        "id": str(e["_id"]),
        "amount": e["amount"],
        "category": e["category"],
        "date": e["date"]
    } for e in expenses]
    return jsonify(result)

@app.route("/expenses/<id>", methods=["DELETE"])
def delete_expense(id):
    result = mongo.db.records.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return jsonify({"msg": "Deleted"}), 200
    return jsonify({"error": "Not found"}), 404

@app.route("/stats", methods=["GET"])
def get_monthly_averages():
    pipeline = [
        {
            "$group": {
                "_id": {
                    "month": {"$substr": ["$date", 0, 7]},
                    "category": "$category"
                },
                "total": {"$sum": "$amount"},
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "month": "$_id.month",
                "category": "$_id.category",
                "average": {
                    "$round": [{"$divide": ["$total", "$count"]}, 2]
                }
            }
        },
        {
            "$sort": {"month": -1, "category": 1}
        }
    ]
    result = list(mongo.db.records.aggregate(pipeline))
    return jsonify(result)

@app.route("/pod", methods=["GET"])
@app.route("/pod/", methods=["GET"])
def identify_pod():
    pod_name = os.environ.get("HOSTNAME", "unknown")
    return jsonify({
        "pod": pod_name,
        "timestamp": datetime.utcnow().isoformat()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
