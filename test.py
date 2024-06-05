import threading
import time

# Định nghĩa hàm sẽ chạy trong luồng
def print_numbers():
    for i in range(1, 6):
        print(f"Number: {i}")
        time.sleep(1)

# Tạo một đối tượng Thread, truyền hàm vào
thread = threading.Thread(target=print_numbers)

# Khởi động luồng
thread.start()

# Thực hiện các công việc khác đồng thời với luồng
for i in range(1, 6):
    print(f"Main thread: {i}")
    time.sleep(0.5)

# Chờ cho luồng kết thúc
thread.join()

print("Luồng đã kết thúc")