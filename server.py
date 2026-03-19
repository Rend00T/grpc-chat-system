import grpc
from concurrent import futures
import threading
import queue

import chat_pb2
import chat_pb2_grpc

# ===== DATABASE SEMENTARA =====
users = set()
online_users = set()
clients = []  # list of queues


# ===== AUTH SERVICE =====
class AuthService(chat_pb2_grpc.AuthServiceServicer):
    def Register(self, request, context):
        if request.username in users:
            return chat_pb2.AuthResponse(success=False, message="User already exists")
        users.add(request.username)
        return chat_pb2.AuthResponse(success=True, message="Register success")

    def Login(self, request, context):
        if request.username not in users:
            return chat_pb2.AuthResponse(success=False, message="User not found")
        online_users.add(request.username)
        return chat_pb2.AuthResponse(success=True, message="Login success")


# ===== USER SERVICE =====
class UserService(chat_pb2_grpc.UserServiceServicer):
    def GetOnlineUsers(self, request, context):
        return chat_pb2.UserList(users=list(online_users))


# ===== CHAT SERVICE (FIXED BROADCAST) =====
class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def ChatStream(self, request_iterator, context):
        q = queue.Queue()
        clients.append(q)

        def receive_messages():
            try:
                for message in request_iterator:
                    print(f"{message.username}: {message.message}")

                    # broadcast ke semua client
                    for client_queue in clients:
                        client_queue.put(message)
            except:
                pass

        threading.Thread(target=receive_messages, daemon=True).start()

        try:
            while True:
                message = q.get()
                yield chat_pb2.ChatMessage(
                    username=message.username,
                    message=message.message
                )
        except:
            clients.remove(q)


# ===== RUN SERVER =====
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    chat_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    chat_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server running on port 50051...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()