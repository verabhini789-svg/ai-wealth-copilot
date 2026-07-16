def get_macro_data() -> dict:
    """
    Returns the current macroeconomic signals and international indicators.
    In the future, this can be connected to real financial APIs.
    """
    repo_rate = 6.50
    inflation_rate = 4.2
    
    # Simple rule-based macro sentiment:
    # If interest rates are low (< 4%) or inflation is high, favor Equities.
    # If interest rates are high (> 5.5%), recommend maintaining cash.
    if repo_rate > 5.5:
        signal = "Markets Favor Cash & Yield"
        color = "var(--color-gold)"
    else:
        signal = "Markets Favor Growth"
        color = "var(--color-success)"
        
    return {
        "kpis": {
            "rbi_repo": f"{repo_rate:.2f}%",
            "inflation": f"{inflation_rate:.1f}%",
            "us_fed": "5.25%",
            "nifty_pe": "22.4x"
        },
        "signal": {
            "label": signal,
            "color": color,
            "description": (
                f"Elevated RBI Repo Rate ({repo_rate:.2f}%) means cash or liquid funds currently earn ~7% risk-free. "
                "Holding 10-15% in cash is highly rational to buy market dips."
            )
        },
        "global_pulse": [
            {"signal": "USD/INR", "current": "₹83.6", "impact": "Weak rupee -> import inflation", "status": "Watch", "badge": "badge-yellow"},
            {"signal": "Crude Oil (Brent)", "current": "$79/bbl", "impact": "High oil -> CAD pressure", "status": "Watch", "badge": "badge-yellow"},
            {"signal": "FII Flows (Jul)", "current": "+₹4,200 Cr", "impact": "Positive sentiment", "status": "Bullish", "badge": "badge-green"},
            {"signal": "US 10Y Bond", "current": "4.35%", "impact": "Capital flows to US bonds", "status": "Caution", "badge": "badge-red"},
            {"signal": "China PMI", "current": "50.4", "impact": "Mild global demand", "status": "Neutral", "badge": "badge-teal"},
            {"signal": "Gold (MCX)", "current": "₹73,400/10g", "impact": "Safe-haven demand", "status": "Hedge", "badge": "badge-green"}
        ]
    }

# Tech cycle database
GADGET_DATABASE = {
    "iphone": {
        "name": "iPhone",
        "verdict": "WAIT",
        "color": "var(--color-error)",
        "reason": "iPhone 17 launches in September 2026. Current iPhone 16 will drop 20-25% in price. Wait for launch.",
        "savings_pct": 0.20,
        "savings_text": "20% (~₹15,000 savings on flagships)"
    },
    "laptop": {
        "name": "Laptop",
        "verdict": "CHECK CHIP",
        "color": "var(--color-gold)",
        "reason": "Intel Arrow Lake and AMD Ryzen AI series launching Q3 2026. M5 MacBooks expected Oct 2026. Wait if buying premium.",
        "savings_pct": 0.15,
        "savings_text": "15% + next-gen performance leap"
    },
    "gpu": {
        "name": "Graphics Card",
        "verdict": "WAIT",
        "color": "var(--color-error)",
        "reason": "NVIDIA RTX 5070/5080 series launching Q4 2026. Current RTX 40-series prices will drop 25-35%.",
        "savings_pct": 0.30,
        "savings_text": "30% (~₹15,000 - ₹30,000 savings)"
    },
    "tablet": {
        "name": "Tablet",
        "verdict": "BUY NOW",
        "color": "var(--color-success)",
        "reason": "iPad Pro M4 is fresh in its cycle. Android tablets (Samsung Tab S9) are well-priced. Good time to buy.",
        "savings_pct": 0.0,
        "savings_text": "Stable pricing - buy now"
    },
    "ssd": {
        "name": "SSD / Storage",
        "verdict": "BUY NOW",
        "color": "var(--color-success)",
        "reason": "NAND flash supply is stabilizing, meaning prices are at multi-year lows. Buy now before prices firm up.",
        "savings_pct": 0.0,
        "savings_text": "Prices at floor - buy now"
    },
    "monitor": {
        "name": "Monitor",
        "verdict": "BUY NOW",
        "color": "var(--color-success)",
        "reason": "OLED monitor market is mature. High-refresh panels from LG/Samsung are excellent value right now.",
        "savings_pct": 0.0,
        "savings_text": "Stable market - buy now"
    }
}

def check_gadget_purchase(category: str, budget: float) -> dict:
    """
    Checks if a gadget is worth buying now or if the user should wait.
    Calculates the 10-year opportunity cost of the potential savings at 15% CAGR.
    """
    g = GADGET_DATABASE.get(category.lower())
    if not g:
        return {
            "verdict": "UNKNOWN",
            "color": "var(--color-text-muted)",
            "reason": "Category not found in release cycle database.",
            "savings": "N/A",
            "opportunity_cost": ""
        }
        
    savings_amt = budget * g["savings_pct"]
    
    # Math: Compounding the savings over 10 years at 15% return
    # Formula: Future Value = Savings * (1.15)^10
    future_value = savings_amt * ((1.15) ** 10)
    
    opportunity_cost_text = ""
    if savings_amt > 0:
        opportunity_cost_text = (
            f"If you wait and save ₹{savings_amt:,.2f}, investing that saved amount "
            f"at 15% CAGR over 10 years grows to **₹{future_value:,.2f}**."
        )
    else:
        opportunity_cost_text = "No immediate savings from waiting, buy if needed."
        
    return {
        "name": g["name"],
        "verdict": g["verdict"],
        "color": g["color"],
        "reason": g["reason"],
        "savings": g["savings_text"],
        "opportunity_cost": opportunity_cost_text
    }

if __name__ == "__main__":
    # Test checking an iPhone purchase with a budget of 80,000
    res = check_gadget_purchase("iphone", 80000)
    print(f"Gadget: {res['name']}")
    print(f"Verdict: {res['verdict']}")
    print(f"Reason: {res['reason'].replace('₹', 'Rs.')}")
    print(f"Savings: {res['savings'].replace('₹', 'Rs.')}")
    print(f"Opp Cost: {res['opportunity_cost'].replace('₹', 'Rs.')}")
