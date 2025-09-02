import json

# Example: suppose 'result' is a Python dictionary or a list
result = {

# Save to JSON file
with open("extracted_entities.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print("✅ Data saved to extracted_entities.json")