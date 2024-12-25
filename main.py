from fastapi import FastAPI, HTTPException, Query
from tools.db import DatabaseSMS

app = FastAPI()
DB_NAME = "sms.db"
db = DatabaseSMS(f"sqlite:///{DB_NAME}")

@app.post("/save")
async def save_item(
    receiver: str,
    uid: int,
    sender: str,
    time: int,
    subject: str = "",
    text: str = ""
):
    """
    Сохраняет SMS в базу данных.
    """
    try:
        db.add_sms(uid=uid, receiver=receiver, sender=sender, time=time, subject=subject, text=text)
        return {"message": "SMS saved successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving SMS: {e}")

@app.get("/get")
async def get_sms(
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
