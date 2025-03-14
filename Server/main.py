import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time
import requests
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../IOT/.env")

# MQTT Broker settings
BROKER = "broker.EMQX.io"
PORT = 1883
BASE_TOPIC = os.getenv("BASE_TOPIC")
# BASE_TOPIC = "alli/ece140/sensors"
# TOPIC = BASE_TOPIC + "/#"
TOPIC = f"{BASE_TOPIC}/#"


# if BASE_TOPIC == "alli/ece140/sensors":
#     print("Please enter a unique topic for your server")
#     exit()


def on_connect(client, userdata, flags, rc):
    """Callback for when the client connects to the broker."""
    if rc == 0:
        print("Successfully connected to MQTT broker")
        client.subscribe(TOPIC)
        print(f"Subscribed to {TOPIC}")
    else:
        print(f"Failed to connect with result code {rc}")

API_ENDPOINT_URL = "http://0.0.0.0:8000/api/sensor_data/add"
# API_ENDPOINT_URL = "http://localhost:6543/api/temperature"
prev_request_time = 0
def on_message(client, userdata, msg):
    """Callback for when a message is received."""
    global prev_request_time
    try:
        # Parse JSON message
        payload = json.loads(msg.payload.decode())
        current_time = datetime.now()
        
        # check the topic if it is the base topic + /readings
        # if it is, print the payload
        # print(payload)
        if msg.topic == (BASE_TOPIC + "/readings"):
            # print("Payload: " , payload)

            # EXTRACTION
            temperature = payload.get("temperature")
            
            # CHECKER:
            if temperature is not None:
                if time.time() - prev_request_time >= 5 :
                    response = requests.post(API_ENDPOINT_URL, json=temperature)

                    if response.status_code == 201:
                        print("SUCCESSFUL: Data sent", response)
                    else:
                        print("FAILURE: Cannot send data", response.text)
                
                    prev_request_time = time.time()
                
        
    except json.JSONDecodeError:
        print(f"\nReceived non-JSON message on {msg.topic}:")
        print(f"Payload: {msg.payload.decode()}")




def main():
    # Create MQTT client
    print("Creating MQTT client...")
    client = mqtt.Client()

    # Set the callback functions onConnect and onMessage
    print("Setting callback functions...")
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        # Connect to broker
        print("Connecting to broker...")
        client.connect(BROKER, PORT, 60) # 60 is timeout option
        
        # Start the MQTT loop
        print("Starting MQTT loop...")
        client.loop_forever()            # press CTRL C to break loop 
        
    except KeyboardInterrupt:
        print("\nDisconnecting from broker...")
        # make sure to stop the loop and disconnect from the broker
        client.loop_stop()
        client.disconnect()
        print("Exited successfully")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

# import paho.mqtt.client as mqtt
# import json
# from datetime import datetime
# import time
# import httpx
# import requests
# from dotenv import load_dotenv
# import os
# import sys
# import asyncio

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from app.database import get_topic_by_user

# load_dotenv(dotenv_path="../IOT/.env")

# # MQTT Broker settings
# BROKER = "broker.EMQX.io"
# PORT = 1883
# BASE_TOPIC = os.getenv("BASE_TOPIC")
# # BASE_TOPIC = "alli/ece140/sensors"
# # TOPIC = BASE_TOPIC + "/#"
# TOPIC = f"{BASE_TOPIC}/#"

# API_ADD_DATA_URL = "http://0.0.0.0:8000/api/sensor_data/add"
# USER_ID_API = "http://0.0.0.0:8000/api/userId"
# subscribed_topics = []

# async def get_user_id():
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(USER_ID_API)
#             if response.status_code == 200:
#                 user_id = response.json().get("userId")
#                 print(f"User ID: {user_id}")
#                 return user_id
#     except httpx.RequestError as e:
#         print(f"Error fetching user ID:", {e})
#     return None

# async def get_device_topics(user_id):
#     devices = await get_topic_by_user(user_id)
#     print(f"Devices: {devices}")
#     if devices:
#         return [device["id"] for device in devices]
#     return []

# # if BASE_TOPIC == "alli/ece140/sensors":
# #     print("Please enter a unique topic for your server")
# #     exit()

# def on_connect(client, userdata, flags, rc):
#     """Callback for when the client connects to the broker."""
#     if rc == 0:
#         print("Successfully connected to MQTT broker")

#         loop = asyncio.get_event_loop()
#         # loop.create_task(subscribe_to_topics(client))
#         asyncio.run_coroutine_threadsafe(subscribe_to_topics(client), asyncio.get_event_loop())


#         # user_id = get_user_id()
#         # if user_id:
#         #     topics = await get_device_topics(user_id)
#         #     for topic in topics:
#         #         if topic not in subscribed_topics:
#         #             TOPIC = f"{BASE_TOPIC}/{topic}"
#         #             client.subscribe(TOPIC)
#         #             subscribed_topics.append(TOPIC)
#         #             print(f"Subscribed to {TOPIC}")
#     else:
#         print(f"Failed to connect with result code {rc}")

# async def subscribe_to_topics(client):
#     user_id = await get_user_id()
#     if not user_id:
#         print("Failed to get user ID, retrying...")
#         return
#     topics = await get_device_topics(user_id)
#     if not topics:
#         print("No topics found for user.")
#         return
#     for topic in topics:
#         topic_path = f"{BASE_TOPIC}/{topic}"
#         if topic not in subscribed_topics:
#             client.subscribe(topic_path)
#             subscribed_topics.append(topic_path)
#             print(f"Subscribed to {topic_path}")

# API_ENDPOINT_URL = "http://0.0.0.0:8000/api/sensor_data/add"
# # API_ENDPOINT_URL = "http://localhost:6543/api/temperature"
# prev_request_time = 0
# def on_message(client, userdata, msg):
#     """Callback for when a message is received."""
#     global prev_request_time
#     try:
#         # Parse JSON message
#         payload = json.loads(msg.payload.decode())
        
#         # check the topic if it is the base topic + /readings
#         # if it is, print the payload
#         # print(payload)
#         topic_parts = msg.topic.split("/")
#         # print("Payload: " , payload)

#         # EXTRACTION
#         # device_id = topic_parts[1]
#         device_id = topic_parts[-1]
#         temperature = payload.get("temperature")
        
#         if temperature is not None and time.time() - prev_request_time >= 5:
#             # asyncio.create_task(send_temperature_data(device_id, temperature))
#             asyncio.run_coroutine_threadsafe(send_temperature_data(device_id, temperature), asyncio.get_event_loop())
#             prev_request_time = time.time()

#         # CHECKER:
#         # if temperature is not None:
#         #     if time.time() - prev_request_time >= 5 :
#         #         data = {
#         #             "device_id": device_id,
#         #             "value": temperature,
#         #         }
#         #         response = requests.post(API_ENDPOINT_URL, json=data)
#         #         if response.status_code == 200:
#         #             print("SUCCESSFUL: Data sent", data)
#         #         else:
#         #             print("FAILURE: Cannot send data", response.text)
            
#         #         prev_request_time = time.time()
                
        
#     except json.JSONDecodeError:
#         print(f"\nReceived non-JSON message on {msg.topic}:")
#         print(f"Payload: {msg.payload.decode()}")


# async def send_temperature_data(device_id, temperature):
#     data = {
#         "device_id": device_id,
#         "value": temperature,
#     }
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.post(API_ADD_DATA_URL, json=data)
#             if response.status_code == 200:
#                 print("SUCCESSFUL: Data sent", data)
#             else:
#                 print("FAILURE: Cannot send data", response.text)
#         except httpx.RequestError as e:
#             print(f"Error sending temperature data: {e}")
# def main():
#     # Create MQTT client
#     print("Creating MQTT client...")
#     client = mqtt.Client()

#     # Set the callback functions onConnect and onMessage
#     print("Setting callback functions...")
#     client.on_connect = on_connect
#     client.on_message = on_message

#     print("Connecting to broker...")
#     client.connect(BROKER, PORT, 60)

#     client.loop_start()
#     asyncio.run(subscribe_to_topics(client))
    
#     try:
#         while True:
#             time.sleep(1)
#         # Connect to broker
#         # print("Connecting to broker...")
#         # client.connect(BROKER, PORT, 60) # 60 is timeout option
        
#         # # Start the MQTT loop
#         # print("Starting MQTT loop...")
#         # client.loop_forever()            # press CTRL C to break loop 
        
#     except KeyboardInterrupt:
#         print("\nDisconnecting from broker...")
#         # make sure to stop the loop and disconnect from the broker
#         client.loop_stop()
#         client.disconnect()
#         print("Exited successfully")
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     main()