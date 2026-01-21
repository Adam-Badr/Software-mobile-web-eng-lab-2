# gpt.py
import json
from openai import OpenAI

client = OpenAI()

CATEGORIES = [
    "Meals",
    "Transport",
    "Lodging",
    "Office Supplies",
    "Entertainment",
    "Other",
]


def extract_receipt_info(image_b64):
    """Extract structured receipt fields from a base64-encoded image via OpenAI.

    The model is prompted to return exactly one JSON object containing:
    - date (str or null)
    - amount (str or null)
    - vendor (str or null)
    - category (str in CATEGORIES or null)

    Args:
        image_b64 (str): Base64-encoded receipt image bytes (no data URL prefix).

    Returns:
        dict: Parsed JSON object with keys: "date", "amount", "vendor", "category".

    Raises:
        json.JSONDecodeError: If the model output is not valid JSON.
        openai.OpenAIError: If the OpenAI API request fails (network/auth/rate-limit/etc.).
        Exception: Any other unexpected error raised by the OpenAI client.
    """
    prompt = f"""
You are an information extraction system.
Extract ONLY the following fields from the receipt image:

date: the receipt date as a string
amount: the total amount paid as it appears on the receipt
vendor: the merchant or vendor name
category: one of [{", ".join(CATEGORIES)}]

Return EXACTLY one JSON object with these four keys and NOTHING ELSE.
Do not include explanations, comments, or formatting.
Do not wrap the JSON in markdown.
If a field cannot be determined, use null.

The output must be valid JSON.
"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        seed=43,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                    },
                ],
            }
        ],
    )
    output = json.loads(response.choices[0].message.content)
    return sanity_check(output)



def sanity_check(jsonString):
    if not isinstance(jsonString, dict):
        return jsonString

    amount = jsonString.get("amount", None)
    if amount is None:
        return jsonString
    
    if isinstance(amount, (int, float)):
        jsonString["amount"] = float(amount)
        return jsonString
    
    if not isinstance(amount, str):
        return jsonString
    
    s = s.replace("$", "")
    try:
        jsonString["amount"] = float(s)
    except Exception:
        pass
    return jsonString