====================== README.md ======================
[![Unlicense License][license-shield]][license-url]

# Software, Mobile and Web engineering lab 1 Assignment

This project extracts structured information from receipt images using OpenAI’s vision models.  
Given a directory of receipt images, it produces a JSON object containing, for each image:

- `date` – the receipt date  
- `amount` – the total paid  
- `vendor` – the merchant name  
- `category` – one of: Meals, Transport, Lodging, Office Supplies, Entertainment, Other  
---

## How it works

1. Each image in the target directory is read and base64-encoded.
2. The encoded image is sent to the OpenAI API with a strict extraction prompt.
3. The model returns **only** a JSON object with the four required fields.
4. All results are aggregated into a single JSON structure keyed by filename.

## Requirements

- Python 3.x 

If you use a virtual environment:

```bash
python -m venv venv  
source venv/bin/activate   # macOS / Linux  
# venv\\Scripts\\activate    # Windows  
pip install -r requirements.txt
```

---

## Configuration

This program requires an environment variable called KEY.

You can provide it by pasting your key as an environment variable:

```bash
export OPENAI_API_KEY=<your key>

```

---

## Usage

To run the program with the --print:
```bash
make run
```

---

## Project Structure

.
├── Makefile
├── README.md
├── requirements.txt
├── receipts/
│   ├── drive.webp
│   ├── receipt_1_food.jpg
│   └── receipt_2_food.png
│   └── walmart.png
└── src/
    ├── __init__.py
    ├── main.py
    └── gpt.py
    └── file_io.py

---

## Notes

====================== Makefile ======================

.PHONY: run

run:
	@python main.py --print