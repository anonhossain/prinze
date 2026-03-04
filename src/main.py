from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

# ────────────────────────────────────────────────
#                  FUNCTION
# ────────────────────────────────────────────────

def career_selection(
    carriers_data: dict,
    shipment_data: dict,
    model: str = "gpt-5.2", # "gpt-5.2" does not exist; using o1 for reasoning
    reasoning_effort: str = "high", # Added reasoning_effort as a parameter
    
) -> str:
    """
    Price recommendation function for clothing sizes based on destination and price.
    """

    # Optional: reasoning_effort is supported by specific o-series models
    reasoning_effort = reasoning_effort

    prompt = f"""\
You are a logistics optimization expert.

Available carriers:
{carriers_data}

New shipment to assign:
{shipment_data}

Choose the SINGLE best carrier for this shipment.
Consider:
• vehicle type / capacity vs shipment requirements
• current availability
• active & total jobs (avoid overloading very busy carriers)
• average rating
• verification status
• transport modes they recently handled

Output format — only the carrier ID, nothing else:

<id>
"""

    try:
        # FIX: The messages list must be INSIDE the create() parentheses
        response = client.chat.completions.create(
            model=model,
            reasoning_effort=reasoning_effort,
            messages=[
                {"role": "system", "content": "Your output ONLY ids: <career_id> nothing else."},
                {"role": "user", "content": prompt}
            ]
        )
    #     response = client.chat.completions.create(
    #     model=model,
    #     reasoning_effort=reasoning_effort,
    #     messages=[
    #         # Remove or comment this line — it's forcing single-line price only
    #         # {"role": "system", "content": "You output ONLY one price range: $10-$20, $20-$30, etc. — nothing else."},
            
    #         {"role": "system", "content": "You are a helpful logistics expert. Follow the output format exactly as instructed in the user message."},  # Optional safe replacement
            
    #         {"role": "user", "content": prompt}
    #     ]
    # )

        prediction = response.choices[0].message.content.strip().upper()
        return prediction

    except Exception as e:
        return f"Error: {str(e)}"
    
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
Provide a realistic USD shipping price range (narrow: low budget to low + < $100) and estimated delivery days based on input.

### INPUT DATA
- Origin: {initial_destination}
- Destination: {final_destination}
- Weight: {weight} kg
- Method: {shipping_method}
- Dimensions: {dimensions}

### KEY RULES
- For 'Air':
  - Budget consolidated air freight (airport-to-airport, forwarders): lower price, 5-12 days
  - Premium express (FedEx/UPS/DHL door-to-door): higher price, 1-5 days
- Chargeable weight: max(actual kg, (L×W×H cm)/5000–6000) if dimensions given
- Include 2026 fuel surcharges (20-35%), handling fees, market indexes
- For sea: reference Drewry/Xeneta, 25-55 days
- Output ONLY the two lines below — no extra text

### OUTPUT
$[Low Estimate (budget)] - $[High Estimate (premium)] 
[low days]-[high days] days

Recommended price range:"""

    try:
        # FIX: The messages list must be INSIDE the create() parentheses
        # response = client.chat.completions.create(
        #     model=model,
        #     reasoning_effort=reasoning_effort,
        #     messages=[
        #         {"role": "system", "content": "You output ONLY one price range: $10-$20, $20-$30, etc. — nothing else."},
        #         {"role": "user", "content": prompt}
        #     ]
        # )
        response = client.chat.completions.create(
        model=model,
        reasoning_effort=reasoning_effort,
        messages=[
            # Remove or comment this line — it's forcing single-line price only
            # {"role": "system", "content": "You output ONLY one price range: $10-$20, $20-$30, etc. — nothing else."},
            
            {"role": "system", "content": "You are a helpful logistics expert. Follow the output format exactly as instructed in the user message."},  # Optional safe replacement
            
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
    dimensions = "50x40x30 cm"

    # Carrier data (as a list of dictionaries)
    carriers_data = [
        {
            "id": 6,
            "is_active": True,
            "is_available": False,
            "vehicle_mode": "van",
            "average_rating": 4.21,
            "service_areas": {
                "Germany": ["Munich", "Frankfurt"],
                "Netherlands": ["Amsterdam", "Rotterdam"]
            }
        },
        {
            "id": 7,
            "is_active": True,
            "is_available": True,
            "vehicle_mode": "truck",
            "average_rating": 4.67,
            "service_areas": {
                "Italy": ["Rome", "Milan"],
                "Switzerland": ["Zurich"]
            }
        },
        {
            "id": 8,
            "is_active": False,
            "is_available": False,
            "vehicle_mode": "trailer",
            "average_rating": 3.45,
            "service_areas": {
                "Spain": ["Madrid", "Barcelona"],
                "Portugal": ["Lisbon"]
            }
        },
        {
            "id": 9,
            "is_active": True,
            "is_available": True,
            "vehicle_mode": "pickup",
            "average_rating": 4.02,
            "service_areas": {
                "Belgium": ["Brussels", "Antwerp"],
                "Germany": ["Cologne"]
            }
        },
        {
            "id": 10,
            "is_active": True,
            "is_available": False,
            "vehicle_mode": "truck",
            "average_rating": 3.92,
            "service_areas": {
                "France": ["Marseille", "Nice"],
                "Italy": ["Turin"]
            }
        },
        {
            "id": 11,
            "is_active": False,
            "is_available": True,
            "vehicle_mode": "van",
            "average_rating": 4.55,
            "service_areas": {
                "Austria": ["Vienna"],
                "Germany": ["Stuttgart", "Dresden"]
            }
        }
    ]

    # Shipment data (as a dictionary)
    shipment_data = {
        "id": 786,
        "receiver_name": "Perferendis veniam",
        "receiver_phone": "+1 (314) 477-6535",
        "receiver_email": "zatumyx@mailinator.com",
        "receiver_address": "Qui in vel error eve",
        "tracking_id": "PERCB6D5EACB128",
        "shipper_id": 14,
        "from_location": "Dolorum est quia des",
        "to_location": "Sed aliqua Sapiente",
        "weight": 17.0,
        "dimensions": "Molestiae modi et do",
        "category": {
            "id": 4,
            "name": "Clothing",
            "description": "Apparel and textiles"
        },
        "estimated_price": "$280 - $360",
        "final_price": None,
        "transport_mode": "air",
        "special_requirements": "Sint consectetur s",
        "status": "matching",
        "timeline_events": [],
        "shipment_created": "2026-03-03 08:47:04",
        "carrier_assigned": True,
        "assigned_carrier": None,
        "estimated_delivery_date": None,
        "carrier_assigned_at": "2026-03-03 08:47:04",
        "updated_at": "2026-03-03T08:47:04.515792Z",
        "documents": [
            {
                "id": 110,
                "document": "http://10.10.13.73:8080/media/shipment_documents/screencapture-localhost-5173-2026-02-27-15_27_13_1_PTOshi8.png",
                "uploaded_at": "2026-03-03T08:47:04.519603Z"
            },
            {
                "id": 111,
                "document": "http://10.10.13.73:8080/media/shipment_documents/screencapture-localhost-5173-channels-2026-02-27-15_31_17_EAcQkiZ.png",
                "uploaded_at": "2026-03-03T08:47:04.522574Z"
            },
            {
                "id": 112,
                "document": "http://10.10.13.73:8080/media/shipment_documents/screencapture-localhost-5173-privacy-2026-02-27-15_31_51_0pu1S0c.png",
                "uploaded_at": "2026-03-03T08:47:04.525379Z"
            },
            {
                "id": 113,
                "document": "http://10.10.13.73:8080/media/shipment_documents/screencapture-localhost-5173-profile-2026-02-27-15_31_43_acSsFLr.png",
                "uploaded_at": "2026-03-03T08:47:04.528270Z"
            }
        ]
    }

    # Prediction for transport price
    # prediction = transport_price_prediction(
    #     initial_destination=initial_destination,
    #     final_destination=final_destination,
    #     weight=weight,
    #     shipping_method=shipping_method,
    #     dimensions=dimensions
    # )
    # print(prediction)

    # Career selection based on provided data
    career_selection = career_selection(
        carriers_data=carriers_data,
        shipment_data=shipment_data
    )
    print(career_selection)