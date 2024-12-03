import os
import json
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.WARNING, format="%(message)s")


def extract_text(soup, keyword):
    """
    Извлекает текст из HTML-структуры, соответствующий ключевому слову.
    """
    element = soup.find(string=lambda x: x and keyword in x)
    if element and ":" in element:
        return element.split(":", 1)[1].strip()
    else:
        logging.warning(f"Warning: Keyword '{keyword}' not found or invalid format.")
        return None


def parse_html(file_path):
    """
    Парсит HTML-файл и извлекает данные.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    city = extract_text(soup, "Город:")
    building = extract_text(soup, "Строение:")

    street_raw = extract_text(soup, "Улица:")
    index = extract_text(soup, "Индекс:")
    street = None

    if street_raw:
        street_parts = street_raw.split("Индекс:")
        street = street_parts[0].strip()
        if len(street_parts) > 1:
            index = street_parts[1].strip()

    floors = extract_text(soup, "Этажи:")

    year_built_span = soup.find("span", class_="year")
    year_built = None
    if year_built_span:
        year_built_text = year_built_span.get_text()
        if "Построено в" in year_built_text:
            year_built = int(year_built_text.replace("Построено в", "").strip())

    parking = extract_text(soup, "Парковка:")
    rating = extract_text(soup, "Рейтинг:")
    views = extract_text(soup, "Просмотры:")

    try:
        floors = int(floors) if floors else None
        rating = float(rating) if rating else None
        views = int(views) if views else None
    except ValueError as e:
        logging.warning(f"Warning: Error converting values in file {file_path}. {e}")

    return {
        "city": city,
        "building": building,
        "street": street,
        "index": index,
        "floors": floors,
        "year_built": year_built,
        "parking": parking,
        "rating": rating,
        "views": views,
    }


def save_to_json(data, filename):
    """
    Сохраняет данные в JSON-файл.
    """
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def main(input_folder, output_folder):
    """
    Парсит все HTML-файлы из папки, сохраняет результат в JSON и выполняет анализ данных.
    """
    data = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".html"):
            file_path = os.path.join(input_folder, filename)
            parsed_data = parse_html(file_path)
            data.append(parsed_data)

    save_to_json(data, os.path.join(output_folder, "parsed_data.json"))

    sorted_data = sorted(
        data,
        key=lambda x: x["year_built"] if x["year_built"] is not None else float("inf"),
    )
    save_to_json(sorted_data, os.path.join(output_folder, "sorted_by_year.json"))

    filtered_data = [item for item in data if item.get("parking") == "есть"]
    save_to_json(filtered_data, os.path.join(output_folder, "filtered_parking.json"))

    views = [item["views"] for item in data if item["views"] is not None]
    stats = {
        "sum": sum(views),
        "min": min(views) if views else None,
        "max": max(views) if views else None,
        "average": sum(views) / len(views) if views else None,
    }
    save_to_json(stats, os.path.join(output_folder, "views_statistics.json"))

    city_frequency = {}
    for item in data:
        city = item.get("city")
        if city:
            city_frequency[city] = city_frequency.get(city, 0) + 1
    save_to_json(city_frequency, os.path.join(output_folder, "city_frequency.json"))


if __name__ == "__main__":
    input_folder = "C:/ProjectsPython/ID_Praktika_3/first_task"
    output_folder = "C:/ProjectsPython/ID_Praktika_3/first_task"

    os.makedirs(output_folder, exist_ok=True)
    main(input_folder, output_folder)
