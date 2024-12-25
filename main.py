import base64
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
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


class GetSMSFilters(BaseModel):
    receiver: str = None
    sender: str = None
    time_start: int = None
    text_contains: str = None


@app.post("/get")
async def get_sms(filters: GetSMSFilters):
    try:
        time_range = (filters.time_start, None) if filters.time_start else None
        sms_list = db.get_sms(
            receiver=filters.receiver,
            sender=filters.sender,
            time_range=time_range,
            text_contains=filters.text_contains,
        )

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
