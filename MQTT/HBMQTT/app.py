import logging
import asyncio
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_0, QOS_1, QOS_2

async def test_coro():
    C = MQTTClient()
    await  C.connect('mqtt://broker.emqx.io/')
    tasks = [
        asyncio.ensure_future(C.publish('a/b', b'TEST MESSAGE WITH QOS_0', qos=QOS_0)),
        asyncio.ensure_future(C.publish('a/b', b'TEST MESSAGE WITH QOS_1', qos=QOS_1)),
        asyncio.ensure_future(C.publish('a/b', b'TEST MESSAGE WITH QOS_2', qos=QOS_2)),
    ]
    await asyncio.wait(tasks)
    logging.info("messages published")
    await C.disconnect()

if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter)
    asyncio.get_event_loop().run_until_complete(test_coro())
    
async def uptime_coro():
    C = MQTTClient()
    await C.connect('mqtt://broker.emqx.io/')
    await C.subscribe([
            ('$SYS/broker/uptime', QOS_1),
            ('$SYS/broker/load/#', QOS_2),
         ])
    try:
            for i in range(1, 100):
                message = await C.deliver_message()
                packet = message.publish_packet
                print(f"{i}:  {packet.variable_header.topic_name} => {packet.payload.data}")
                
            await C.unsubscribe(['$SYS/broker/uptime', '$SYS/broker/load/#'])
            await C.disconnect()
            except ClientException as ce:
            logging.error("Client exception: %s" % ce)

if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=formatter)
    asyncio.get_event_loop().run_until_complete(uptime_coro())