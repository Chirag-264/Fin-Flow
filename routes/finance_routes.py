from flask import Blueprint, request, jsonify
from ml.ml_model import predict_future_expenses, recommend_investments, ai_assistant_response
from database import get_db_connection

finance_routes = Blueprint("finance_routes", __name__)

# Route: Predict Future Expenses
@finance_routes.route("/predict_expenses", methods=["GET"])
def predict_expenses():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    prediction = predict_future_expenses(user_id)
    return jsonify({"future_expenses": prediction})

# Route: Investment Recommendations
@finance_routes.route("/investment_recommendation", methods=["GET"])
def investment_recommendation():
    recommendations = recommend_investments()
    return jsonify({"investment_recommendations": recommendations})

# Route: AI Financial Assistant Response
@finance_routes.route("/ai_assistant", methods=["POST"])
def ai_assistant():
    data = request.get_json()
    user_input = data.get("user_input")

    if not user_input:
        return jsonify({"error": "User input is required"}), 400

    response = ai_assistant_response(user_input)
    return jsonify({"assistant_response": response})

# Route: Fetch User Financial Data
@finance_routes.route("/user_financials/<int:user_id>", methods=["GET"])
def user_financials(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT balance, total_expenses, total_income FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user_data:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user_data)
