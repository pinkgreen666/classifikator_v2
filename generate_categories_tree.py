import csv
import json
from loguru import logger


input_file = "company_category_manual_202508060605_1.csv"
output_file = "categories_tree.json"

companies_data = {}

try:
    with open(input_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            company_id = row["company_id"]
            if company_id not in companies_data:
                companies_data[company_id] = []
            companies_data[company_id].append(row)
except Exception as e:
    logger.error(f"Error: {e}")

categories_tree = {}

for company_id, categories in companies_data.items():
    nodes = {cat["id"]: {**cat, "children": []} for cat in categories}

    tree = []
    for cat_id, node in nodes.items():
        parent_id = node.get("parent_id")
        if parent_id and parent_id in nodes:
            nodes[parent_id]["children"].append(node)
        else:
            tree.append(node)

    categories_tree[company_id] = tree

json_output = json.dumps(categories_tree, indent=4, ensure_ascii=False)

try:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(json_output)
    logger.success(f"Result in {output_file}")

except Exception as e:
    logger.error(f"Error: {e}")