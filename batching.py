import json
import os
from loguru import logger

input_file = "categories_tree_only_names.json"
output_dir = "output"

os.makedirs(output_dir, exist_ok=True)

try:
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for key, value in data.items():
        item_data = { key: value }

        output_file = os.path.join(output_dir, f"{key}.json")

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(item_data, f, ensure_ascii=False, indent=4)
            logger.success(f"Result in {output_file}")
        except Exception as e:
            logger.error(f"Error: {e}")
    
except Exception as e:
    logger.error(f"Error: {e}")
