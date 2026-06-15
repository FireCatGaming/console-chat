import asyncio
import websockets
import os

clients = set()

async def handler(ws):
    try:
        nick = await ws.recv()
        clients.add(ws)

        print(nick, "подключился")

        while True:
            message = await ws.recv()

            dead = set()

            for client in clients:
                try:
                    await client.send(message)
                except:
                    dead.add(client)

            for d in dead:
                clients.discard(d)

    except Exception as e:
        print("Ошибка:", e)

    finally:
        clients.discard(ws)
        print("отключился")

async def main():
    PORT = int(os.environ.get("PORT", 10000))

    async with websockets.serve(handler, "0.0.0.0", PORT):
        print("Server started", PORT)
        await asyncio.Future()

asyncio.run(main())
