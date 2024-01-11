import qrcode

# QR 코드에 포함할 데이터
data = "SJBIKE_03367"

# QR 코드 생성
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# 데이터 추가
qr.add_data(data)
qr.make(fit=True)

# QR 코드 이미지 생성
img = qr.make_image(fill_color="black", back_color="white")

# 이미지 저장 또는 표시
img.save("qr_code.png")