import os
import json
import google.generativeai as genai

def generate_ai_advice(api_key: str, age: int, risk: str, capital: float, allocation: dict, gadget_category: str = None, gadget_budget: float = 0.0) -> dict:
    """
    Sends the user context and allocation numbers to Gemini AI.
    Returns a structured JSON response with out-of-the-box wealth roadmaps.
    """
    # 1. If no API key is passed, check environment variables (secure for cloud hosting)
    if not api_key or api_key.strip() == "":
        api_key = os.environ.get("GEMINI_API_KEY", "")
        
    # If still no key, fall back to mock data
    if not api_key or api_key.strip() == "":
        return get_mock_advice(age, risk, capital, allocation, gadget_category, gadget_budget)
        
    try:
        # 2. Configure Gemini API
        genai.configure(api_key=api_key)
        
        # We extract the specific dollar amounts to tell the AI exactly how much cash is in each bucket
        stocks_amt = allocation["dollars"]["Equities (Stocks)"]
        reit_amt = allocation["dollars"]["Real Estate (REITs)"]
        cash_amt = allocation["dollars"]["Safe Cash"]
        skills_amt = allocation["dollars"]["Self-Growth (Education)"]
        
        # 3. Create the CFO prompt template
        prompt = f"""
        You are the AI Wealth Copilot, an elite out-of-the-box Personal CFO and Wealth Advisor.
        Your goal is to help the user grow their net worth not just through standard investments, but through high-ROI skills and avoiding consumer traps.
        
        User Profile:
        - Age: {age}
        - Total Capital: INR {capital:,.2f}
        - Risk Profile: {risk}
        - Current Macro Interest Rate: 6.50% (Repo Rate)
        
        Calculated Asset Allocation:
        - Equities (Stocks): INR {stocks_amt:,.2f} ({allocation['percentages']['Equities (Stocks)']:.1f}%)
        - Real Estate (REITs): INR {reit_amt:,.2f} ({allocation['percentages']['Real Estate (REITs)']:.1f}%)
        - Safe Cash (HYSA/T-Bills): INR {cash_amt:,.2f} ({allocation['percentages']['Safe Cash']:.1f}%)
        - Self-Growth (Skills/Courses): INR {skills_amt:,.2f} ({allocation['percentages']['Self-Growth (Education)']:.1f}%)
        
        Planned Gadget Purchase: {gadget_category if gadget_category else "None"}
        Gadget Budget: INR {gadget_budget:,.2f}
        
        Provide your advice strictly in the JSON format requested below. Do not include any formatting marks (like ```json), just return the raw JSON object.
        
        JSON Schema structure to return:
        {{
          "reasoning": "A concise paragraph explaining why this specific allocation is optimal for a {age}-year-old with a {risk} risk tolerance. Reference how high interest rates (6.5%) make holding safe cash attractive.",
          "skills": [
            {{
              "name": "High-ROI Skill 1 (e.g. Web Development, SQL, Copywriting, video editing)",
              "cost": "Cost estimate (e.g. Free on YouTube, INR 2,000 course) which MUST fit inside their Self-Growth budget of INR {skills_amt:,.2f}",
              "why": "How learning this skill generates a 10-100x return on investment compared to passive stock investing."
            }},
            {{
              "name": "High-ROI Skill 2",
              "cost": "Cost estimate",
              "why": "Why this skill expands their earning capacity."
            }}
          ],
          "gadget_comment": "Advice on whether their planned purchase of {gadget_category} at INR {gadget_budget:,.2f} is a good decision. Compare the purchase price to the opportunity cost of investing that money at 15% CAGR over 10 years.",
          "discipline_rule": "A short, actionable psychological rule (e.g., the 48-Hour Rule or the 1-for-1 Investing Rule) to help them remain disciplined."
        }}
        """
        
        # 4. Call the Gemini model
        # We use the 'gemini-1.5-flash' model because it is fast, cheap, and supports structured JSON outputs
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Parse and return the JSON
        return json.loads(response.text)
        
    except Exception as e:
        print(f"Gemini API error: {e}. Falling back to mock advice.")
        return get_mock_advice(age, risk, capital, allocation, gadget_category, gadget_budget)

def get_mock_advice(age: int, risk: str, capital: float, allocation: dict, gadget_category: str = None, gadget_budget: float = 0.0) -> dict:
    """
    Fallback method returning high-quality mock advice if no API key is supplied.
    Matches the JSON structure exactly.
    """
    skills_amt = allocation["dollars"]["Self-Growth (Education)"]
    
    # Pre-crafted high-ROI skills suggestions
    skills_data = [
        {
            "name": "Technical Foundations (SQL & Python)",
            "cost": "Free (YouTube / Kaggle)",
            "why": "Knowing how to query databases and automate tasks increases your entry-level salary in finance and technology by 30-50%."
        },
        {
            "name": "High-Income Sales & Copywriting",
            "cost": "INR 1,500 (Books/Online Courses)",
            "why": "Understanding psychology and communication allows you to freelance or sell startup services, converting your time directly into capital."
        }
    ]
    
    gadget_tip = "No gadget purchase requested. Pro tip: Apply the '1-for-1 Rule'—every time you buy a consumer gadget, force yourself to invest the exact same amount in your stock portfolio."
    if gadget_category:
        saved_amt = gadget_budget * 0.20
        future_val = saved_amt * (1.15 ** 10)
        gadget_tip = (
            f"You are considering a {gadget_category.upper()} with a budget of INR {gadget_budget:,.2f}. "
            f"If you delay purchase to the next launch cycle, you save ~20% (INR {saved_amt:,.2f}). "
            f"Investing that saved amount at 15% CAGR over 10 years yields **INR {future_val:,.2f}** in compounding growth. "
            f"Consider if the immediate convenience beats this long-term growth."
        )
        
    return {
        "reasoning": (
            f"At age {age} with a {risk} risk profile, compounding is your primary wealth driver. "
            f"The 110-minus-age rule allocates the majority of your capital to growth (Equities & REITs). "
            f"Because RBI Repo Rates are high (6.50%), keeping safe cash in High-Yield accounts is smart "
            f"as it currently yields 7% risk-free. Your self-growth allocation of INR {skills_amt:,.2f} "
            "is your highest leverage asset—use it to build high-income skills."
        ),
        "skills": skills_data,
        "gadget_comment": gadget_tip,
        "discipline_rule": "The 48-Hour Rule: Wait 48 hours before executing any non-essential purchase. It breaks the dopamine loop of impulse buying."
    }

if __name__ == "__main__":
    # Test our mock fallback
    from allocation_engine import calculate_allocation
    alloc = calculate_allocation(19, "Moderate", 20000.0)
    res = generate_ai_advice(None, 19, "Moderate", 20000.0, alloc, "iphone", 80000)
    
    print("--- Mock AI Response ---")
    print(json.dumps(res, indent=2))
