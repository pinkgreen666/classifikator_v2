import csv
import json

def build_category_tree(csv_path):
    """
    Считывает категории из CSV-файла и строит иерархическое дерево для каждой компании.

    Args:
        csv_path (str): Путь к вашему CSV-файлу.

    Returns:
        dict: Словарь, где ключи - это ID компаний, а значения -
              список корневых категорий в виде дерева.
    """
    # Словарь для хранения всех строк по company_id
    companies_data = {}

    # Читаем CSV файл с разделителем ";"
    try:
        with open(csv_path, mode='r', encoding='utf-8') as infile:
            # Используем DictReader для удобного доступа к столбцам по их именам
            reader = csv.DictReader(infile, delimiter=';')
            for row in reader:
                company_id = row['company_id']
                if company_id not in companies_data:
                    companies_data[company_id] = []
                companies_data[company_id].append(row)
    except FileNotFoundError:
        return {"error": f"Файл не найден по пути: {csv_path}"}
    except Exception as e:
        return {"error": f"Произошла ошибка при чтении файла: {e}"}

    # Итоговый JSON для всех компаний
    all_companies_tree = {}

    # Обрабатываем данные для каждой компании отдельно
    for company_id, categories in companies_data.items():
        # Создаем словарь для быстрого доступа к категориям по их 'id'
        nodes = {cat['id']: {**cat, 'children': []} for cat in categories}

        # Список для хранения корневых узлов (у которых нет родителя или родитель не в списке)
        tree = []

        for cat_id, node in nodes.items():
            parent_id = node.get('parent_id')
            # Если есть parent_id и он существует в нашем наборе узлов,
            # добавляем текущий узел как дочерний к родителю.
            if parent_id and parent_id in nodes:
                nodes[parent_id]['children'].append(node)
            # В противном случае, это корневой узел для данной компании.
            else:
                tree.append(node)
        
        all_companies_tree[company_id] = tree

    return all_companies_tree

# --- Пример использования ---

# 1. Укажите путь к вашему файлу
csv_file_path = 'company_category_manual_202508060605_1.csv' # <--- ЗАМЕНИТЕ НА ВАШ ПУТЬ

# 2. Постройте дерево
hierarchical_data = build_category_tree(csv_file_path)

# 3. Преобразуйте в красивый JSON и выведите на экран
#    indent=4 делает JSON читабельным
#    ensure_ascii=False для корректного отображения кириллицы
json_output = json.dumps(hierarchical_data, indent=4, ensure_ascii=False)

print(json_output)

# 4. (Опционально) Сохраните результат в файл
try:
    with open('categories_tree.json', 'w', encoding='utf-8') as outfile:
        outfile.write(json_output)
    print("\n✅ Результат успешно сохранен в файл 'categories_tree.json'")
except Exception as e:
    print(f"\n❌ Не удалось сохранить файл: {e}")