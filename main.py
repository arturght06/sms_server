import base64
from fastapi import FastAPI, HTTPException, Request, Query
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


@app.get("/get")
async def get_sms(
    uid: int = Query(None, description="SMS id"),
    receiver: str = Query(None, description="Receiver number"),
    sender: str = Query(None, description="Sender number"),
    time_start: int = Query(None, description="Start time as Unix timestamp"),
    text_contains: str = Query(None, description="Substring to search in text")
):
    """
    Получает SMS из базы данных с применением фильтров.
    """
    try:
        sms_list = db.get_sms(
            uid=uid,
            receiver=receiver,
            sender=sender,
            time_start=time_start,
            text_contains=text_contains
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



