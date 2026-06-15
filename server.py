import asyncio
import websockets

clients = {}

async def handler(ws):
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
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Сервер запущен на 8765")
        await asyncio.Future()

asyncio.run(main())