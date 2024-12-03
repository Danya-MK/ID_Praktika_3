import os
import json
from bs4 import BeautifulSoup
import re
from statistics import mean, stdev


def parse_html(file_path):
    """
    Извлекает данные об объектах из HTML-файла.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    items = []
    product_items = soup.find_all("div", class_="product-item")

    for product in product_items:
        item = {}
        item["id"] = product.find("a", class_="add-to-favorite")["data-id"]
        item["name"] = product.find("span").get_text()
        price_text = product.find("price").get_text()
        item["price"] = int(re.sub(r"[^\d]", "", price_text))
        characteristics = product.find_all("li")
        for char in characteristics:
            char_type = char["type"]
            char_value = char.get_text()
            if char_type in ["ram", "camera", "acc", "sim"]:
                char_value = int(re.sub(r"[^\d]", "", char_value))
            elif char_type == "resolution":
                char_value = char_value.strip()
            item[char_type] = char_value
        items.append(item)
    return items


def save_to_json(data, filename):
    """
    Сохраняет данные в JSON-файл.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def calculate_statistics(data, field):
    """
    Вычисляет статистические показатели для числового поля.
    """
    values = [item[field] for item in data if field in item]
    if not values:
        return {}
    return {
        "sum": sum(values),
        "min": min(values),
        "max": max(values),
        "mean": mean(values),
        "std_dev": stdev(values) if len(values) > 1 else 0,
    }


def count_frequency(data, field):
    """
    Подсчитывает частоту для текстового поля.
    """
    frequency = {}
    for item in data:
        if field in item:
            value = item[field]
            frequency[value] = frequency.get(value, 0) + 1
    return frequency


def main(input_folder, output_folder):
    """
    Главная функция для обработки всех HTML-файлов.
    """
    all_data = []

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".html"):
            file_path = os.path.join(input_folder, file_name)
            all_data.extend(parse_html(file_path))

    save_to_json(all_data, os.path.join(output_folder, "parsed_data.json"))

    sorted_data = sorted(all_data, key=lambda x: x.get("price", 0), reverse=True)
    save_to_json(sorted_data, os.path.join(output_folder, "sorted_by_price.json"))

    filtered_data = [item for item in all_data if item.get("sim", 0) >= 2]
    save_to_json(filtered_data, os.path.join(output_folder, "filtered_by_sim.json"))

    acc_stats = calculate_statistics(all_data, "acc")
    save_to_json(acc_stats, os.path.join(output_folder, "acc_statistics.json"))

    resolution_frequency = count_frequency(all_data, "resolution")
    save_to_json(
        resolution_frequency, os.path.join(output_folder, "resolution_frequency.json")
    )


if __name__ == "__main__":
    input_folder = "C:/ProjectsPython/ID_Praktika_3/second_task"
    output_folder = "C:/ProjectsPython/ID_Praktika_3/second_task"

    os.makedirs(output_folder, exist_ok=True)

    main(input_folder, output_folder)
