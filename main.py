import asyncio
import json
import websockets
import os
from dotenv import load_dotenv

load_dotenv()

def sts_connect():
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise Exception("DEEPGRAM_API_KEY is not found")

    sts_ws = websockets.connect(
        "wss://agent.deepgram.com/v1/agent/converse",
        subprotocols=["token" , api_key]
    )
    return sts_ws

def load_config():
    with open("config.json" , "r") as f:
        return json.load(f)


async def handle_barge_in(decoded , twilio_ws , streamsid):
    pass


async def handle_text_message(decoded , twilio_ws , sts_ws , streamsid):
    pass


async def sts_sender(sts_ws , audio_queue):
    pass


async def sts_reciever(sts_ws , twilio_ws , streamsid_queue):
    pass


async def twilio_reciever(twilio_ws , audio_queue , streamsid_queue):
    pass


async def twilio_handler(twilio_ws):
    pass


async def main():
    await websockets.serve(twilio_handler , host="localhost" , port=5000)
    print("started server .")
    await asyncio.Future()

if __name__ == "__main__" :
    asyncio.run(main())