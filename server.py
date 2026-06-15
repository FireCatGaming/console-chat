import asyncio
import os
import websockets

clients = {}  # websocket -> nickname


async def broadcast(message):
    dead = []

    for client in clients:
        try:
            await client.send(message)
        except:
            dead.append(client)

    for client in dead:
        clients.pop(client, None)


async def handler(ws):
    try:
        # получаем ник при подключении
        nick = await ws.recv()

        clients[ws] = nick

        print(f"{nick} подключился")

        await broadcast(f"🔔 {nick} подключился к чату")

        # получаем сообщения
        while True:
            message = await ws.recv()

            print(message)

            await broadcast(message)

    except Exception as e:
        print("Ошибка:", e)

    finally:
        if ws in clients:
            nick = clients[ws]

            del clients[ws]

            print(f"{nick} отключился")

            await broadcast(f"🔔 {nick} покинул чат")


async def main():
    port = int(os.environ.get("PORT", 10000))

    async with websockets.serve(
        handler,
        "0.0.0.0",
        port
    ):
        print(f"Сервер запущен на порту {port}")

        await asyncio.Future()


asyncio.run(main())
```
