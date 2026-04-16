# TumorSeg-ALPDINO: Phân Vùng U Não với Mô Hình Tự Giám Sát DINOv2
---

## 📄 **BÁO CÁO CHI TIẾT**

> 📌 **Xem báo cáo toàn diện tại đây:** [**Báo cáo.pdf**](./Báo%20cáo.pdf)
> 
> Báo cáo tiểu luận "Phương Pháp Luận Nghiên Cứu Khoa Học" (2025)  
> Tác Giả: **Phạm Ngọc Thắng** | Hướng Dẫn: **TS. Từ Thảo Hương Giang**

---
## Giới Thiệu Dự Án

Dự án này nhằm **cải thiện khả năng phân vùng khối u não** trên ảnh cộng hưởng từ (MRI) thông qua việc tích hợp bộ mã hóa tự giám sát **DINOv2** vào kiến trúc mạng nguyên mẫu thích ứng **ALPNet**, đặc biệt trong **điều kiện dữ liệu hạn chế** (Few-shot Learning).

### Mục Tiêu Chính
- Giảm thiểu sự phụ thuộc vào dữ liệu gán nhãn trong chẩn đoán y tế
- Nâng cao độ chính xác phân vùng u não trong các kịch bản 1-shot và 5-shot
- Chứng minh tính khả thi của chuyển giao tri thức từ mô hình nền tảng sang lĩnh vực y tế

---

##  Kiến Trúc Mô Hình

### DINO-ALPNet
Mô hình kết hợp hai thành phần chính:

```
┌─────────────────────────────────────────┐
│  DINOv2 Encoder (Vision Transformer)    │
│  - Trích xuất đặc trưng tự giám sát      │
│  - Khả năng tổng quát hóa cao            │
└────────────────┬────────────────────────┘
                 │
        ┌────────▼────────┐
        │  Support/Query  │
        │    Features     │
        └────────┬────────┘
                 │
┌────────────────▼────────────────────────┐
│  Adaptive Local Prototypes (ALP)        │
│  - Tạo nguyên mẫu cục bộ thích ứng       │
│  - Xử lý hình thái phức tạp              │
└────────────────┬────────────────────────┘
                 │
        ┌────────▼────────┐
        │ Segmentation Map│
        │  (Decoder)      │
        └─────────────────┘
```

### Thay Thế Encoder
- **Trước**: ResNet-101 (giám sát truyền thống) ~ 70.5M tham số
- **Sau**: ViT-B/14 từ DINOv2 (tự giám sát) ~ 86.0M tham số

---

## 📊 Kết Quả Chính

### Cải Thiện Độ Chính Xác (Dice Score)

| Kịch Bản | ALPNet (Baseline) | DINO-ALPNet | Cải Thiện |
|----------|-------------------|------------|----------|
| **1-Shot** | 65.42% | **71.85%** | ↑ **6.43%** |
| **5-Shot** | 72.15% | **79.30%** | ↑ **7.15%** |

### Độ Ổn Định
- **ALPNet**: Giảm 11.7% khi chuyển từ 5-shot → 1-shot ⚠️
- **DINO-ALPNet**: Giảm chỉ 3.2% 👍

*Điều này chứng minh rằng DINOv2 cung cấp biểu diễn đặc trưng mạnh mẽ hơn, ít phụ thuộc vào lượng dữ liệu mẫu.*

---

## 🎨 Ví Dụ Kết Quả Phân Vùng

**So sánh trực quan:**
- **Baseline (ALPNet)**: Vẫn có nhiều nhiễu xung quanh khối u, đường biên chưa mịn
- **DINO-ALPNet**: Kết quả ổn định hơn, loại bỏ hầu hết nhiễu nền, biên khối u khớp chính xác hơn

### Kết Quả So Sánh
![Segmentation Results Comparison](./images/segmentation_results.jpg)
*Hình 2: So sánh kết quả phân vùng trên một ca bệnh - (a) Ảnh gốc, (b) Nhãn thật, (c) Kết quả ALPNet (Baseline), (d) Kết quả DINO-ALPNet (Cải tiến)*

## 📈 Tập Dữ Liệu

### BraTS 2023 (Brain Tumor Segmentation Challenge)
- **Chuỗi xung MRI**: T1, T1ce (contrast-enhanced), T2, FLAIR
- **Nhiệm vụ**: Phân vùng 3 vùng bệnh lý
  - Lõi u hoại tử (Necrotic core)
  - Vùng phù nề (Edema)
  - Khối u tăng quang (Enhancing tumor)
- **Tiền xử lý**: Chuẩn hóa cường độ, cắt về 224×224

### Ví Dụ Dữ Liệu
![BraTS 2023 Dataset Examples](./images/dataset_samples.jpg)
*Hình 1: Các mẫu dữ liệu từ BraTS 2023 - ảnh MRI đa phương thức với các ca bệnh có u não (Tumor) và không có u não (No Tumor)*

---

## 🛠️ Thiết Lập Kỹ Thuật

### Yêu Cầu
- Python 3.8+
- PyTorch 1.12+
- NVIDIA GPU (RTX 3090 với 24GB VRAM khuyến nghị)

### Cài Đặt Huấn Luyện
- **Optimizer**: AdamW
- **Learning Rate**: 1e⁻⁴
- **Hàm Mất Mát**: Cross-Entropy + Dice Loss
- **Epochs**: 50
- **Episodes/Epoch**: 1,000 (meta-learning)
- **Batch Size**: 24

---

## Những Phát Hiện Chính

### 1. **Khả Năng Biểu Diễn Đặc Trưng**
   - DINOv2 trích xuất đặc trưng tốt hơn bộ mã hóa giám sát truyền thống
   - Giảm tác động của sai lệch miền dữ liệu (domain gap)

### 2. **Hiệu Suất Trong Điều Kiện Ít Dữ Liệu**
   - Cải thiện rõ rệt ở kịch bản 1-shot (+6.43%)
   - Giữ vững lợi thế ở 5-shot (+7.15%)

### 3. **Tính Ổn Định**
   - Mô hình ít nhạy cảm với sự thay đổi lượng dữ liệu
   - Phù hợp cho môi trường y tế với dữ liệu giới hạn

---

## Ý Nghĩa Khoa Học & Thực Tiễn

### Khoa Học
Chứng minh hiệu quả của việc ứng dụng học biểu diễn tự giám sát vào bài toán học ít mẫu, mở rộng hiểu biết về chuyển giao tri thức từ mô hình nền tảng (Foundation Models).

### Thực Tiễn
Cung cấp giải pháp công nghệ khả thi cho:
- Bệnh viện thiếu chuyên gia chẩn đoán hình ảnh
- Các quốc gia có dữ liệu y tế chuẩn hóa hạn chế
- Hệ thống hỗ trợ chẩn đoán tự động với độ chính xác cao

---

## Hướng Phát Triển Tiếp Theo

### 1. **Tối Ưu Hóa Mô Hình**
   - Nén mô hình (model compression) để giảm 86M → ~30-40M tham số
   - Chưng cất tri thức (knowledge distillation)
   - Lượng tử hóa (quantization)
   - **Mục đích**: Triển khai trên máy tính y tế thông thường

### 2. **Đánh Giá Mở Rộng**
   - Kiểm thử trên ảnh CT, X-quang
   - Thử nghiệm với các cơ quan khác (phổi, gan, v.v.)
   - Đánh giá tính tổng quát hóa trên các bộ dữ liệu khác

---

## Tài Liệu Tham Khảo

Báo cáo chi tiết được lưu trong file: **[Báo cáo.pdf](./Báo%20cáo.pdf)**

### Tác Giả
**Phạm Ngọc Thắng** (B22DCKH120)  
Khoa Công Nghệ Thông Tin  
Học viện Công Nghệ Bưu Chính Viễn Thông

### Hướng Dẫn
**TS. Từ Thảo Hương Giang**

### Ngành Học
Phương Pháp Luận Nghiên Cứu Khoa Học  
Tháng 11/2025

---

## 📌 Tóm Tắt Nhanh

| Yếu Tố | Chi Tiết |
|--------|---------|
| **Bài Toán** | Phân vùng u não trong điều kiện dữ liệu ít |
| **Phương Pháp** | DINOv2 encoder + ALPNet decoder |
| **Dữ Liệu** | BraTS 2023 (MRI đa phương thức) |
| **Kết Quả** | +6-7% Dice Score so với baseline |
| **Ưu Điểm** | Ổn định, ít phụ thuộc vào dữ liệu mẫu |
| **Ứng Dụng** | Hỗ trợ chẩn đoán u não tự động |

---

## 🔗 Liên Kết

- **Bộ dữ liệu**: [BraTS 2023](https://www.med.upenn.edu/cbica/brats2023/)
- **DINOv2**: [Facebook Research](https://dinov2.metademolab.com/)
- **ALPNet**: [Few-shot Medical Image Segmentation](https://github.com/PAD13/ALPNet)


