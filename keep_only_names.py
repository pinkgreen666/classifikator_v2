import json
from loguru import logger

def process_node(node):
    if isinstance(node, dict):
        if "name" in node:
            new_node = {"name": node["name"]}
            if "children" in node:
                new_node["children"] = [process_node(child) for child in node["children"]]
            return new_node
        else:
            new_dict = {}
            for key, value in node.items():
                processed_value = process_node(value)
                if processed_value is not None:
                    new_dict[key] = processed_value
            return new_dict if new_dict else None
    elif isinstance(node, list):
        new_list = [process_node(item) for item in node]
        return [item for item in new_list if item is not None]
    else:
        return None

input_file = "categories_tree.json"
output_file = "categories_tree_only_names.json"

try:
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    logger.error(f"Error: {e}")

categories_tree_only_names = process_node(data)

try:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(categories_tree_only_names, f, indent=4, ensure_ascii=False)
    logger.success(f"Result in {output_file}")
except Exception as e:
    logger.error(f"Error: {e}")
