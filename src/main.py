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
    dimensions: str = None
) -> str:
    """
    Price recommendation function for clothing sizes based on destination and price.
    """

    # Optional: reasoning_effort is supported by specific o-series models
    reasoning_effort = "medium" 

    prompt = f"""
### ROLE
You are an elite International Logistics Consultant and Freight Forwarding Expert. 

### TASK
Calculate a realistic, market-accurate shipping price range based on the provided shipment metadata. 

### INPUT DATA
- Origin: {initial_destination}
- Destination: {final_destination}
- Weight: {weight} kg
- Shipping Method: {shipping_method}
- Dimensions: {dimensions}

### CONSTRAINTS & REQUIREMENTS
1. MARKET DATA: Base the estimate on current 2026 global shipping indexes.
2. DIMENSIONS: If dimensions are not provided, assume a standard volumetric weight ratio.
3. SURCHARGES: Factor in estimated fuel surcharges and baseline international handling fees.
4. FORMATTING: You must output ONLY the price range. Do not include currency symbols other than '$'. 
5. PRICE RANGE: Provide a realistic low and high estimate based on the above factors.
6. PRICE SUGGESTION: For air take reference from FedEx/UPS/DHL, for sea take reference from Drewry/Xeneta.

### OUTPUT STRUCTURE
$[Low Estimate]-$[High Estimate] (e.g., $Low Estimate-$High Estimate)

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
    initial_destination = "Singapore"
    final_destination = "USA"
    weight = 10
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
