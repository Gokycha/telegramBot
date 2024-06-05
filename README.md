# Telegram Bot
## Mô tả
Bot telegram này được tạo ra để nhắc nhở ae đi ăn, lên ngủ trưa và về đúng giờ.
Hiện tại chỉ mới có các chức năng cơ bản là hẹn giờ.
Các chức năng khác sẽ được thêm vào trong quá trình phát triển.

## Các thông tin chi tiết về bot
token: **7392075828:AAEfBjUKzgQnrIT4jIkhUV2YzKGxQOnGXDM**
Tên bot: **TimeKeeper**
Username: **ultimate_time_keeper_bot**

## Run bot
Truy cập vào [Github của bot](https://github.com/Gokycha/telegramBot). Vào phần Actions và kích hoạt `workflows`.
Có thể chỉnh sửa file build bot trong `python-app.yml`.

## Chạy bot trên local
Cài đặt [Python](https://www.python.org/downloads/) (nếu chưa có).
Chạy các lệnh sau:
```bash
# tạo biến môi trường
python -m venv venv
# kích hoạt biến môi trường
venv\Scripts\activate.bat
# cài đặt các thư viện
pip install -r requirements.txt
# build bot trên local
py telegramBot.py
```
## Lưu ý
- Có thể chỉnh sửa danh sách các thư viện cần cài trong file `requirements.txt`.