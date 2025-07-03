
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from protonmail import ProtonMail
import os
import signal

app = FastAPI()

username = os.environ['PROTON_MAIL']
password = os.environ['PROTON_PASS']

proton = ProtonMail()

def shutdown():
    pid = os.getpid()
    os.kill(pid, signal.SIGINT)

@app.on_event("startup")
async def startup_event():

    try:
        proton.login(username, password)
        print("Loggin succesful, waiting for request")
    except Exception as e:
        shutdown()




def get_message_by_code(client: ProtonMail, code: str):
    last_messages = client.get_messages()
    for message in last_messages:
        msg = client.read_message(message)
        if code in msg.recipients[0].extra.get('Address', ''):
            return msg
    return None

@app.get("/request/{code}")
def get_email_by_code(code: str):
    try:
        message = get_message_by_code(proton, code)

        if not message:
            raise HTTPException(status_code=404, detail="Message not found")

        return {
            "subject": message.subject,
            "body": message.body
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
