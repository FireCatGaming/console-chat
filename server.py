import asyncio
import os
import websockets

clients = {}  # websocket -> nickname

ADMINS = {
    "FireCat"
}


async def broadcast(message):
    dead = []

    for client in list(clients.keys()):
        try:
            await client.send(message)
        except:
            dead.append(client)

    for client in dead:
        clients.pop(client, None)


async def handler(ws):
    try:
        nick = (await ws.recv()).strip()

        clients[ws] = nick

        print(f"{nick} подключился")

        await broadcast(f"🔔 {nick} подключился к чату")

        while True:
            message = (await ws.recv()).strip()

            # список онлайн
            if message == "/online":
                users = ", ".join(clients.values())
                await ws.send(f"👥 Онлайн: {users}")
                continue

            # кик
            if message.startswith("/kick "):

                if nick not in ADMINS:
                    await ws.send("❌ Нет прав.")
                    continue

                target = message[6:].strip()

                found = False

                for client, client_nick in list(clients.items()):

                    if client_nick == target:

                        await client.send(
                            "🚫 Вы были отключены администратором."
                        )

                        await client.close()

                        found = True
                        break

                if not found:
                    await ws.send("❌ Пользователь не найден.")

                continue

            formatted = f"[{nick}] {message}"

            print(formatted)

            await broadcast(formatted)

    except Exception as e:
        print("Ошибка:", e)

    finally:
        if ws in clients:

            nick = clients[ws]

            del clients[ws]

            print(f"{nick} отключился")

            await broadcast(
                f"🔔 {nick} покинул чат"
            )


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
