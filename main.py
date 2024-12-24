from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
# from typing import List

# Создаем приложение FastAPI
app = FastAPI()


# Определяем модель данных для валидации входных данных
class Item(BaseModel):
    uid: int
    date: int
    subject: str
    text: str
    sender: str
    receiver: str
    service_center: str


# Указываем путь к файлу для записи данных
FILE_PATH = "data.json"


# # Функция для парсинга строки смс
# def parse_sms_string(sms_string: str) -> Item:
#     """
#     Функция для разбора строки смс на нужные элементы.
#     Строка предполагается в формате:
#     "5|3|+48888396164||1734975811742|1734975738000|0|0|-1|1|0||Food|+48601000480|0|0|0|0|-1"
#     """
#     try:
#         # Разбиваем строку на части
#         parts = sms_string.split("|")
#
#         # Проверка на корректность количества частей
#         if len(parts) != 22:
#             raise ValueError("Invalid SMS string format")
#
#         # Создаем объект Item, заполняя поля
#         item = Item(
#             uid=int(parts[0]),  # 5
#             date=int(parts[3]),  # 1734975811742
#             subject=parts[11] if parts[11] else "Unknown",  # Food (subject)
#             text=parts[9] if parts[9] else "",  # Food (body/text)
#             sender=parts[2],  # +48888396164 (sender)
#             service_center=parts[10]  # +48601000480 (service_center)
#         )
#         return item
#     except Exception as e:
#         raise ValueError(f"Error parsing SMS string: {e}")

@app.post("/save")
async def save_item(sms_string: str):
    """
    Обрабатывает POST-запрос, принимает строку смс, парсит её в объект Item и сохраняет в файл.
    """
    try:
        print(sms_string)
        return {"message": "Item saved successfully!"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving item: {e}")


# @app.post("/save")
# async def save_item(sms_string: str):
#     """
#     Обрабатывает POST-запрос, принимает строку смс, парсит её в объект Item и сохраняет в файл.
#     """
#     try:
#         # Парсим строку смс в объект Item
#         item = parse_sms_string(sms_string)
#
#         # Читаем существующие данные из файла (если файл существует)
#         try:
#             with open(FILE_PATH, "r") as file:
#                 data = json.load(file)
#         except FileNotFoundError:
#             data = []
#
#         # Добавляем новый элемент в данные
#         data.append(item.model_dump())  # Преобразуем в словарь и добавляем
#
#         # Сохраняем данные обратно в файл
#         with open(FILE_PATH, "w") as file:
#             json.dump(data, file, indent=4)
#
#         return {"message": "Item saved successfully!"}
#
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error saving item: {e}")


@app.get("/items")
async def get_items():
    """
    Обрабатывает GET-запрос, возвращает все сохраненные данные.
    """
    try:
        with open(FILE_PATH, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {"message": "No data found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading items: {e}")
