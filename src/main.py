from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

# ────────────────────────────────────────────────
#                  FUNCTION
# ────────────────────────────────────────────────

def transport_price_prediction(
    initial_destination: str, # Changed from dict to str to match your usage example
    final_destination: str = None,
    weight: float = 0,
    shipping_method: str = "",
    model: str = "gpt-5.2", # "gpt-5.2" does not exist; using o1 for reasoning
    reasoning_effort: str = "high", # Added reasoning_effort as a parameter
    dimensions: str = None
) -> str:
    """
    Price recommendation function for clothing sizes based on destination and price.
    """

    # Optional: reasoning_effort is supported by specific o-series models
    reasoning_effort = reasoning_effort

    prompt = f"""

### ROLE
You are an elite International Logistics Consultant with 2026 market knowledge.

### TASK
Provide a realistic shipping price range (USD) based on input data. Include both premium express and budget options when applicable.

### INPUT DATA
- Origin: {initial_destination}
- Destination: {final_destination}
- Weight: {weight} kg
- Method: {shipping_method}
- Dimensions: {dimensions}

### KEY RULES
- For 'Air': 
  - Premium express (FedEx/UPS/DHL door-to-door, fast 2-5 days): higher rates
  - Budget consolidated air freight (airport-to-airport via forwarders): lower rates
- Calculate chargeable weight if dimensions given: max(actual kg, (L×W×H cm)/5000–6000)
- Factor 2026 fuel surcharges (~20-35%), handling fees, market indexes.
- If sea: reference Drewry/Xeneta.
- Output ONLY the range — no extra text. Let the range be between lower price and lower price + less then 100 USD

### OUTPUT
$[Low Estimate (budget)] - $[High Estimate (premium)] 

Recommended price range:"""

    try:
        # FIX: The messages list must be INSIDE the create() parentheses
        response = client.chat.completions.create(
            model=model,
            reasoning_effort=reasoning_effort,
            messages=[
                {"role": "system", "content": "You output ONLY one price range: $10-$20, $20-$30, etc. — nothing else."},
                {"role": "user", "content": prompt}
            ]
        )
        
        prediction = response.choices[0].message.content.strip().upper()
        return prediction

    except Exception as e:
        return f"Error: {str(e)}"

# ────────────────────────────────────────────────
#                  USAGE EXAMPLE
# ────────────────────────────────────────────────

if __name__ == "__main__":
    # Matches your provided inputs
    initial_destination = "Dhaka"
    final_destination = "London"
    weight = 60
    shipping_method = "Air"
    dimensions = "50x40x30 cm"  # Optional, not used in current prompt but can be added to the prompt if needed

    prediction = transport_price_prediction(
        initial_destination=initial_destination,
        final_destination=final_destination,
        weight=weight,
        shipping_method=shipping_method,
        dimensions=dimensions
    )
    print(prediction)
