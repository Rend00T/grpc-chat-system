import grpc
import chat_pb2
import chat_pb2_grpc
import threading

def run():
    channel = grpc.insecure_channel('localhost:50051')

    auth_stub = chat_pb2_grpc.AuthServiceStub(channel)
    chat_stub = chat_pb2_grpc.ChatServiceStub(channel)

    username = input("Enter username: ")

    # register dulu (biar gak error user not found)
    auth_stub.Register(chat_pb2.AuthRequest(username=username))

    # login
    response = auth_stub.Login(chat_pb2.AuthRequest(username=username))
    print(response.message)

    if not response.success:
        return

    def send_messages():
        while True:
            msg = input()
            yield chat_pb2.ChatMessage(username=username, message=msg)

    def receive_messages():
        responses = chat_stub.ChatStream(send_messages())
        for res in responses:
            print(f"\n{res.username}: {res.message}")

    threading.Thread(target=receive_messages, daemon=True).start()

    # supaya program tidak langsung exit
    while True:
        pass


if __name__ == '__main__':
    run()