from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MongoDB container hostname is "mongo" (from docker-compose)
app.config["MONGO_URI"] = "mongodb://mongo:27017/expenses"
mongo = PyMongo(app)

@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()

    # Safely convert amount to float
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
    expenses = list(mongo.db.records.find({}, {"_id": 0}))
    return jsonify(expenses)

@app.route("/stats", methods=["GET"])
def get_monthly_averages():
    pipeline = [
        {
            "$group": {
                "_id": {
                    "month": {"$substr": ["$date", 0, 7]},  # e.g., "2025-06"
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
