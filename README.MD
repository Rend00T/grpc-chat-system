# 💬 Real-Time Chat System using gRPC (Python)

## 📌 Deskripsi

Project ini merupakan implementasi sistem chat real-time menggunakan gRPC dengan arsitektur client-server dan multi-service. Sistem ini memungkinkan banyak client untuk saling berkomunikasi secara langsung menggunakan bidirectional streaming.

---

## 🎯 Tujuan

* Mengimplementasikan komunikasi menggunakan gRPC
* Menggunakan Bidirectional Streaming untuk chat real-time
* Menerapkan arsitektur multi-service
* Mendukung multi-client
* Mengelola state menggunakan in-memory server

---

## 🏗️ Arsitektur Sistem

Sistem terdiri dari 3 service utama:

* **AuthService** → Register & Login user
* **ChatService** → Mengelola komunikasi chat real-time
* **UserService** → Menampilkan daftar user online

---

## ⚙️ Teknologi yang Digunakan

* Python 3
* gRPC (`grpcio`, `grpcio-tools`)
* Protocol Buffers (`.proto`)

---

## 📁 Struktur Folder

```
project/
│   server.py
│   client.py
│   chat_pb2.py
│   chat_pb2_grpc.py
│   README.md
│
└── proto/
    └── chat.proto
```

---

## 🔧 Cara Setup

### 1. Install Dependency

Pastikan Python sudah terinstall, lalu jalankan:

```
pip install grpcio grpcio-tools
```

---

### 2. Generate File gRPC (jika belum ada)

```
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/chat.proto
```

---

## 🚀 Cara Menjalankan

### 1. Jalankan Server

```
python server.py
```

Output:

```
Server running on port 50051...
```

---

### 2. Jalankan Client (Minimal 2 Terminal)

Buka terminal baru:

```
python client.py
```

Masukkan username:

```
Enter username: raihan
```

---

### 3. Jalankan Client Kedua

```
python client.py
```

Masukkan username lain:

```
Enter username: asep
```

---

## 💬 Cara Menggunakan

* Ketik pesan di salah satu client
* Tekan Enter
* Pesan akan muncul di semua client secara real-time

Contoh:

```
raihan: halo asep
asep: halo juga
```

---

## ✅ Fitur yang Diimplementasikan

* Unary RPC (Login & Register)
* Bidirectional Streaming (Real-Time Chat)
* Multi Client Support
* Multi Service Architecture
* In-Memory State Management
* Error Handling (user exist / not found)

---

## ⚠️ Catatan

* User akan otomatis di-register saat login pertama
* Server harus dijalankan terlebih dahulu sebelum client
* Gunakan minimal 2 client untuk melihat fitur real-time

---

## 👨‍💻 Author

* Nama: [Isi Nama Kamu & Kelompok]
* Mata Kuliah: Integrasi Sistem
* Semester: 4

---

## 🚀 Status Project

✅ Fully Working
✅ Ready for Demo
✅ Meets All Requirements

---
