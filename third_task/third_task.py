import os
import json
import xml.etree.ElementTree as ET
from statistics import mean, stdev


def parse_xml(file_path):
    """
    Парсит XML-файл и извлекает данные об объекте.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    def extract_text(tag_name):
        element = root.find(tag_name)
        return element.text.strip() if element is not None else None

    name = extract_text("name")
    constellation = extract_text("constellation")
    spectral_class = extract_text("spectral-class")
    radius = extract_text("radius")
    rotation = extract_text("rotation")
    age = extract_text("age")
    distance = extract_text("distance")
    absolute_magnitude = extract_text("absolute-magnitude")

    try:
        radius = int(radius) if radius else None
        rotation = float(rotation.split()[0]) if rotation else None
        age = float(age.split()[0]) if age else None
        distance = float(distance.split()[0]) if distance else None
        absolute_magnitude = (
            float(absolute_magnitude.split()[0]) if absolute_magnitude else None
        )
    except ValueError:
        pass

    return {
        "name": name,
        "constellation": constellation,
        "spectral_class": spectral_class,
        "radius": radius,
        "rotation": rotation,
        "age": age,
        "distance": distance,
        "absolute_magnitude": absolute_magnitude,
    }


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
    values = [item[field] for item in data if field in item and item[field] is not None]
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
        if field in item and item[field] is not None:
            value = item[field]
            frequency[value] = frequency.get(value, 0) + 1
    return frequency


def main(input_folder, output_folder):
    """
    Главная функция для обработки всех XML-файлов.
    """
    all_data = []

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".xml"):
            file_path = os.path.join(input_folder, file_name)
            all_data.append(parse_xml(file_path))

    save_to_json(all_data, os.path.join(output_folder, "parsed_data.json"))

    sorted_data = sorted(all_data, key=lambda x: x.get("radius", 0), reverse=True)
    save_to_json(sorted_data, os.path.join(output_folder, "sorted_by_radius.json"))

    filtered_data = [item for item in all_data if item.get("age", 0) > 0.5]
    save_to_json(filtered_data, os.path.join(output_folder, "filtered_by_age.json"))

    distance_stats = calculate_statistics(all_data, "distance")
    save_to_json(
        distance_stats, os.path.join(output_folder, "distance_statistics.json")
    )

    constellation_frequency = count_frequency(all_data, "constellation")
    save_to_json(
        constellation_frequency,
        os.path.join(output_folder, "constellation_frequency.json"),
    )


if __name__ == "__main__":
    input_folder = "C:/ProjectsPython/ID_Praktika_3/third_task"
    output_folder = "C:/ProjectsPython/ID_Praktika_3/third_task"

    os.makedirs(output_folder, exist_ok=True)

    main(input_folder, output_folder)
