# Bài kiểm tra nhanh giữa kỳ

Đề bài: Xây dựng một Todo app với các chức năng:
1. Tạo mới một todo
2. Lấy danh sách todo
3. Cập nhật todo
4. Xoá todo

Yêu cầu thoả mãn đủ các đầu API:
- Tạo mới todo: `POST /todos`
- Lấy danh sách todo: `GET /todos`
- Cập nhật todo: `PUT /todos/{id}`
- Xoá todo: `DELETE /todos/{id}`

Với id dưới dạng UUID.

Format trả về của các API:
- Tạo mới todo:
```json
{
  "id": "uuid",
  "title": "string",
  "completed": false
}
```
- Lấy danh sách todo:
```json
[
  {
    "id": "uuid",
    "title": "string",
    "completed": false,
    "created_at": "2023-10-01 00:00:00",
    "updated_at": "2023-10-01 00:00:00"
  },
  ...
]
```
- Cập nhật todo:
Payload gửi lên trong body, sử dụng dạng JSON:
```json
{
  "title": "string",
  "completed": false
}
```
Kết quả trả về:
```json
{
  "id": "uuid",
  "title": "string",
  "completed": false,
  "updated_at": "2023-10-01 00:00:00"
}
```
- Xoá todo:
```json
{
  "message": "Todo deleted successfully"
}
```
