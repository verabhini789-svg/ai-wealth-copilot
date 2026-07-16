def calculate_allocation(age: int, risk_tolerance: str, total_capital: float) -> dict:
    """
    Calculates the asset allocation percentages and dollar amounts
    based on the '110 minus Age' rule adjusted for risk tolerance.
    
    Parameters:
    - age (int): The age of the user.
    - risk_tolerance (str): 'Conservative', 'Moderate', or 'Aggressive'.
    - total_capital (float): The total capital to invest.
    
    Returns:
    - dict: A dictionary with allocation percentages and dollar amounts for:
      - Equities (Stocks)
      - Real Estate (REITs)
      - Safe Cash (High-Yield Savings)
      - Self-Growth (Skills/Education)
    """
    # 1. Calculate Base Growth allocation (110 minus Age)
    base_growth = 110 - age
    
    # 2. Adjust based on Risk Tolerance
    # Aggressive moves 15% more into Growth.
    # Conservative moves 15% out of Growth into Safe Assets.
    if risk_tolerance.lower() == "aggressive":
        growth_target = base_growth + 15
    elif risk_tolerance.lower() == "conservative":
        growth_target = base_growth - 15
    else: # Moderate / Default
        growth_target = base_growth
        
    # Boundary controls: Ensure Growth is never 100% or 0%
    # We always want to keep at least 5% in safe assets for emergencies
    growth_target = max(5.0, min(90.0, growth_target))
    safe_target = 100.0 - growth_target
    
    # 3. Divide the Growth Portion:
    # We allocate 70% of the growth portion to Stocks, 30% to Real Estate (REITs)
    pct_equities = (growth_target * 0.70)
    pct_real_estate = (growth_target * 0.30)
    
    # 4. Divide the Safe Portion:
    # We allocate 90% of the safe portion to Cash, 10% to Self-Growth (Skills/Courses)
    pct_cash = (safe_target * 0.90)
    pct_self_growth = (safe_target * 0.10)
    
    # Calculate exact dollar amounts
    dollar_equities = total_capital * (pct_equities / 100.0)
    dollar_real_estate = total_capital * (pct_real_estate / 100.0)
    dollar_cash = total_capital * (pct_cash / 100.0)
    dollar_self_growth = total_capital * (pct_self_growth / 100.0)
    
    return {
        "percentages": {
            "Equities (Stocks)": pct_equities,
            "Real Estate (REITs)": pct_real_estate,
            "Safe Cash": pct_cash,
            "Self-Growth (Education)": pct_self_growth
        },
        "dollars": {
            "Equities (Stocks)": dollar_equities,
            "Real Estate (REITs)": dollar_real_estate,
            "Safe Cash": dollar_cash,
            "Self-Growth (Education)": dollar_self_growth
        }
    }

if __name__ == "__main__":
    # Test the logic with a sample profile (19 years old, 20,000 capital, Moderate Risk)
    sample_age = 19
    sample_risk = "Moderate"
    sample_capital = 20000.0
    
    allocation = calculate_allocation(sample_age, sample_risk, sample_capital)
    
    print(f"--- Allocation for Age {sample_age}, {sample_risk} Risk, ${sample_capital:,.2f} Capital ---")
    for asset, pct in allocation["percentages"].items():
        usd = allocation["dollars"][asset]
        print(f" - {asset:25} : {pct:5.1f}% | ${usd:8,.2f}")
