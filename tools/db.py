from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class SMS(Base):
    __tablename__ = 'sms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    receiver = Column(String, nullable=False)
    sender = Column(String, nullable=False)
    time = Column(Integer, nullable=False)
    subject = Column(String)
    text = Column(Text)

class DatabaseSMS:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_sms(self, uid: int, receiver: str, sender: str, time: int, subject: str, text: str):
        session = self.Session()
        try:
            exists = session.query(SMS).filter_by(
                id=uid,
                receiver=receiver,
                sender=sender,
                time=time,
                subject=subject,
                text=text
            ).first()

            if exists:
                print(f"Message {uid} already exists in DB!")
                return

            sms = SMS(id=uid, receiver=receiver, sender=sender, time=time, subject=subject, text=text)
            session.add(sms)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_sms(self, uid: int = None, receiver: str = None, sender: str = None, time_start: int = None, text_contains: str = None):
        session = self.Session()
        try:
            query = session.query(SMS)
            if uid:
                query = query.filter(SMS.id == uid)
            if receiver:
                query = query.filter(SMS.receiver == receiver)
            if sender:
                query = query.filter(SMS.sender == sender)
            if time_start:
                query = query.filter(SMS.time >= time_start)
            if text_contains:
                query = query.filter(SMS.text.contains(text_contains))

            return query.all()
        finally:
            session.close()