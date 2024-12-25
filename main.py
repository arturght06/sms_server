import base64
from fastapi import FastAPI, HTTPException, Request
from tools.db import DatabaseSMS

app = FastAPI()
DB_NAME = "sms.db"
db = DatabaseSMS(f"sqlite:///{DB_NAME}")


@app.post("/save")
async def save_item(request: Request):
    """
    Обрабатывает POST-запрос, принимает строку смс, парсит её в объект Item и сохраняет в файл.
    """
    try:
        body = (await request.body()).decode("utf-8")
        body = base64.b64decode(body).decode("utf-8")
        receiver, uid, sender, time, subject, text = body.split("|", 5)
        db.add_sms(uid=int(uid), receiver=receiver, sender=sender, time=int(time), subject=subject, text=text)
        return {"message": "SMS saved successfully!"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving item: {e}")


@app.post("/get")
async def get_sms(request: Request):
    """
    Получает список SMS по указанным фильтрам.
    """
    try:
        body = await request.json()
        receiver = body.get("receiver")
        sender = body.get("sender")
        time_start = body.get("time_start")
        text_contains = body.get("text_contains")

        # Фильтры для запроса к базе данных
        filters = {}
        if receiver:
            filters['receiver'] = receiver
        if sender:
            filters['sender'] = sender
        if time_start:
            filters['time_range'] = (time_start,)
        if text_contains:
            filters['text_contains'] = text_contains

        sms_list = db.get_sms(**filters)

        return [
            {
                "id": sms.id,
                "receiver": sms.receiver,
                "sender": sms.sender,
                "time": sms.time,
                "subject": sms.subject,
                "text": sms.text,
            }
            for sms in sms_list
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving SMS: {e}")


