from bs4 import BeautifulSoup
import json
import os
import statistics

file_path = "Београд _ Екатеринбург.html"
with open(file_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

products = []
for item in soup.find_all("script", type="application/ld+json"):
    try:
        data = json.loads(item.string)
        if isinstance(data, dict) and data.get("@type") == "ItemList":
            for product in data["itemListElement"]:
                product_info = product["item"]
                name = product_info.get("name", "")
                description = product_info.get("description", "")
                price = float(product_info["offers"][0]["price"])
                products.append(
                    {
                        "name": name,
                        "description": description,
                        "price": price,
                    }
                )
    except (json.JSONDecodeError, KeyError):
        continue


sorted_products = sorted(products, key=lambda x: x["price"])

filtered_products = [p for p in products if p["price"] > 100]

prices = [p["price"] for p in products]
price_stats = {
    "sum": sum(prices),
    "min": min(prices),
    "max": max(prices),
    "average": statistics.mean(prices) if prices else None,
}

word_frequency = {}
for product in products:
    words = product["description"].split()
    for word in words:
        word_frequency[word] = word_frequency.get(word, 0) + 1

output_folder = "results"
os.makedirs(output_folder, exist_ok=True)

products_path = os.path.join(output_folder, "parsed_products.json")
with open(products_path, "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=4)

sorted_products_path = os.path.join(output_folder, "sorted_products.json")
with open(sorted_products_path, "w", encoding="utf-8") as f:
    json.dump(sorted_products, f, ensure_ascii=False, indent=4)

filtered_products_path = os.path.join(output_folder, "filtered_products.json")
with open(filtered_products_path, "w", encoding="utf-8") as f:
    json.dump(filtered_products, f, ensure_ascii=False, indent=4)

price_stats_path = os.path.join(output_folder, "price_stats.json")
with open(price_stats_path, "w", encoding="utf-8") as f:
    json.dump(price_stats, f, ensure_ascii=False, indent=4)

word_frequency_path = os.path.join(output_folder, "word_frequency.json")
with open(word_frequency_path, "w", encoding="utf-8") as f:
    json.dump(word_frequency, f, ensure_ascii=False, indent=4)
