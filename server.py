import asyncio
import websockets
import os

clients = {}

async def handler(ws, path):
    try:
        nick = await ws.recv()
        clients[ws] = nick

        print(f"{nick} подключился")

        async for message in ws:
            print(message)

            dead = []

            for client in clients:
                try:
                    await client.send(message)
                except:
                    dead.append(client)

            for d in dead:
                clients.pop(d, None)

    except:
        pass

    finally:
        if ws in clients:
            print(f"{clients[ws]} отключился")
            del clients[ws]

async def main():
    PORT = int(os.environ.get("PORT", 8765))

    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"Сервер запущен на {PORT}")
        await asyncio.Future()

asyncio.run(main())
