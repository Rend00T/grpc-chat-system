import grpc
import chat_pb2
import chat_pb2_grpc
import threading
from datetime import datetime

def run():
    channel = grpc.insecure_channel('localhost:50051')

    auth_stub = chat_pb2_grpc.AuthServiceStub(channel)
    chat_stub = chat_pb2_grpc.ChatServiceStub(channel)
    user_stub = chat_pb2_grpc.UserServiceStub(channel)

    username = input("Enter username: ")

    # register dulu (biar tidak error user not found)
    auth_stub.Register(chat_pb2.AuthRequest(username=username))

    # login
    response = auth_stub.Login(chat_pb2.AuthRequest(username=username))
    print(response.message)

    if not response.success:
        return

    def send_messages():
        while True:
            try:
                msg = input()

                # ===== COMMAND /online =====
                if msg.strip() == "/online":
                    response = user_stub.GetOnlineUsers(chat_pb2.Empty())
                    print("\n[Online Users]:")
                    for user in response.users:
                        print(f"- {user}")
                    continue  # aman sekarang karena dalam try loop

                # ===== KIRIM CHAT =====
                timestamp = datetime.now().strftime("%H:%M")
                yield chat_pb2.ChatMessage(
                    username=username,
                    message=msg,
                    timestamp=timestamp
                )

            except Exception as e:
                print("Error sending message:", e)
                break

    def receive_messages():
        try:
            responses = chat_stub.ChatStream(send_messages())
            for res in responses:
                print(f"\n[{res.timestamp}] {res.username}: {res.message}")
        except Exception as e:
            print("Connection error:", e)

    # jalankan thread untuk menerima pesan
    threading.Thread(target=receive_messages, daemon=True).start()

    # supaya program tetap hidup
    while True:
        pass


if __name__ == '__main__':
    run()