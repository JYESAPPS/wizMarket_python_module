from PIL import Image
import os
import shutil

SOURCE_BASE = r"C:\Users\jyes_semin\Desktop\Data\Design\77"
DEST_BASE = r"C:\workspace\back\wizMarket_ads_be\app\uploads\thumbnail\77"
TARGET_SIZE = (400, 400)
JPEG_QUALITY = 85
SUPPORTED_EXT = [".png", ".jpg", ".jpeg"]

def process_folder(folder_name):
    src_folder = os.path.join(SOURCE_BASE, folder_name)
    dst_folder = os.path.join(DEST_BASE, folder_name)

    if not os.path.exists(dst_folder):
        print(f"❌ 대상 폴더 없음: {dst_folder}")
        return

    # 이미지 파일만 필터링 및 정렬 (예: 1.jpg, 2.png ...)
    image_files = sorted([
        f for f in os.listdir(src_folder)
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXT
    ])

    for idx, file in enumerate(image_files, start=1):
        ext = os.path.splitext(file)[1].lower()
        src_path = os.path.join(src_folder, file)
        renamed_filename = f"thumbnail_{idx}{ext}"
        renamed_path = os.path.join(src_folder, renamed_filename)

        # ✅ 원본 리네임
        os.rename(src_path, renamed_path)

        # ✅ 썸네일 생성 (.jpg 저장)
        try:
            with Image.open(renamed_path) as img:
                img = img.convert("RGB")
                img = img.resize(TARGET_SIZE, Image.LANCZOS)
                thumb_path = os.path.join(src_folder, f"thumbnail_{idx}_thumb.jpg")
                img.save(thumb_path, "JPEG", quality=JPEG_QUALITY)
                print(f"✅ 썸네일 저장됨: {thumb_path}")
        except Exception as e:
            print(f"❌ 이미지 처리 에러: {renamed_path} -> {e}")

    # ✅ 리네임된 원본 + 썸네일 복사
    for file in os.listdir(src_folder):
        src_file = os.path.join(src_folder, file)
        dst_file = os.path.join(dst_folder, file)
        shutil.copy2(src_file, dst_file)
        print(f"📁 복사됨: {src_file} → {dst_file}")

# ✅ 1~6 폴더 반복 처리
for i in range(1, 7):
    process_folder(str(i))
