import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Import our custom financial modules
from allocation_engine import calculate_allocation
from macro_analyser import get_macro_data, check_gadget_purchase
from advisor_prompt import generate_ai_advice

# Initialize the Flask application
app = Flask(__name__, static_folder='.')
# Enable CORS so our local index.html file is allowed to speak to us
CORS(app)

@app.route('/')
def serve_index():
    """
    Serves the main index.html file when visiting http://127.0.0.1:5000/
    """
    return send_from_directory('.', 'index.html')

@app.route('/api/macro', methods=['GET'])
def api_macro():
    """
    Endpoint that returns current macroeconomic indicators.
    """
    return jsonify(get_macro_data())

@app.route('/api/allocate', methods=['POST'])
def api_allocate():
    """
    Core API Endpoint: Receives user details, calculates allocations,
    runs the tech cycle check, calls Gemini AI, and returns the full advisor report.
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400
        
    # Extract values from request (use sensible defaults if missing)
    age = int(data.get("age", 25))
    risk_tolerance = data.get("risk_tolerance", "Moderate")
    total_capital = float(data.get("total_capital", 100000.0))
    gadget_category = data.get("gadget_category", None)
    gadget_budget = float(data.get("gadget_budget", 0.0))
    api_key = data.get("api_key", "") # Passed securely from client session state
    
    # 1. Run the Math Allocation Engine
    alloc = calculate_allocation(age, risk_tolerance, total_capital)
    
    # 2. Run the Tech Cycle Checker (if user specified a gadget purchase)
    gadget_info = None
    if gadget_category and gadget_category.strip() != "":
        gadget_info = check_gadget_purchase(gadget_category, gadget_budget)
        
    # 3. Call the AI Advisor Prompt Engine (will use Gemini API or mock fallback)
    ai_advice = generate_ai_advice(
        api_key=api_key,
        age=age,
        risk=risk_tolerance,
        capital=total_capital,
        allocation=alloc,
        gadget_category=gadget_category,
        gadget_budget=gadget_budget
    )
    
    # 4. Package and send back the results
    return jsonify({
        "allocation": alloc,
        "gadget_info": gadget_info,
        "ai_advice": ai_advice
    })

if __name__ == "__main__":
    print("Starting AI Wealth Copilot Flask backend...")
    # Read the PORT assigned by Render, defaulting to 5000 for local development
    port = int(os.environ.get("PORT", 5000))
    print(f"Open http://127.0.0.1:{port} in your browser to view the application.")
    app.run(host="0.0.0.0", port=port, debug=True)
