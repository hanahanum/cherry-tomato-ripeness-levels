# Menyesuaikan Ukuran Tiap Gambar 

import cv2
import os

input_folder = 'photos'
output_folder = 'cv-output'
target_size = (800, 800)  # Sesuaikan ukuran yang diinginkan

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)
        resized_img = cv2.resize(img, target_size)
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, resized_img)



# Menampilkan Hasil Prediksi JSON 

import requests
import json
import os

api_key = "ROBOFLOW_API_KEY"
model_id = "ROBOFLOW_MODEL_ID"
version = "ROBOFLOW_MODEL_VERSION"

url = f"https://detect.roboflow.com/{model_id}/{version}?api_key={api_key}"

output_folder = 'cv-output-new'
result_folder = 'predicted'



if not os.path.exists(result_folder):
    os.makedirs(result_folder)

for filename in os.listdir(output_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        file_path = os.path.join(output_folder, filename)
        
        with open(file_path, "rb") as file:
            response = requests.post(url, files={"file": file})
            
            if response.status_code == 200:
                result = response.json()

                # Inisialisasi ulang kamus deteksi untuk setiap gambar
                detections_count = {
                    "fine": 0,
                    "unripe": 0,
                    "overripe": 0,
                    "damaged": 0
                }

                # Loop melalui prediksi untuk menghitung deteksi
                for prediction in result['predictions']:
                    label = prediction['class']
                    if label in detections_count:
                        detections_count[label] += 1

                # Tambahkan jumlah deteksi ke hasil JSON
                result['detections_count'] = detections_count

                # Simpan hasil JSON ke file
                result_filename = os.path.splitext(filename)[0] + ".json"
                result_path = os.path.join(result_folder, result_filename)
                
                with open(result_path, 'w') as result_file:
                    json.dump(result, result_file, indent=4)
                print(f"Hasil prediksi untuk {filename} berhasil disimpan di {result_path}")
            else:
                print(f"Error {response.status_code} untuk file {filename}: {response.text}")

# Cetak jumlah deteksi total untuk setiap kelas setelah semua gambar diproses
total_detections = {
    "fine": 0,
    "unripe": 0,
    "overripe": 0,
    "damaged": 0
}

# Loop lagi untuk menghitung total deteksi dari semua file JSON
for filename in os.listdir(result_folder):
    if filename.endswith('.json'):
        result_path = os.path.join(result_folder, filename)
        with open(result_path, 'r') as result_file:
            data = json.load(result_file)
            # Tambahkan pemeriksaan kunci di sini
            if 'detections_count' in data:
                for label, count in data['detections_count'].items():
                    total_detections[label] += count
            else:
                print(f"'detections_count' tidak ditemukan dalam file {filename}")

print("\nJumlah deteksi total untuk setiap kelas dari semua gambar:")
for label, count in total_detections.items():
    print(f"{label}: {count}")


import requests
import json
import os
import cv2

api_key = "ROBOFLOW_API_KEY"
model_id = "ROBOFLOW_MODEL_ID"
version = "ROBOFLOW_MODEL_VERSION"

url = f"https://detect.roboflow.com/{model_id}/{version}?api_key={api_key}"

output_folder = 'cv-output-new'
result_folder = 'predicted'

# Menampilkan Hasil Prediksi Gambar

if not os.path.exists(result_folder):
    os.makedirs(result_folder)


# Tetapkan warna BGR untuk setiap kelas
COLORS = {
    "fine": (0, 255, 255),    # Kuning
    "unripe": (0, 255, 0),    # Hijau
    "overripe": (0, 0, 255),  # Merah
    "damaged": (42, 42, 165)  # Coklat
}

for filename in os.listdir(output_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        file_path = os.path.join(output_folder, filename)
        
        with open(file_path, "rb") as file:
            response = requests.post(url, files={"file": file})
            
            if response.status_code == 200:
                result = response.json()

                # Baca gambar asli
                image = cv2.imread(file_path)

                # Loop melalui prediksi untuk menggambar bounding box
                for prediction in result['predictions']:
                    x = int(prediction['x'])
                    y = int(prediction['y'])
                    width = int(prediction['width'])
                    height = int(prediction['height'])
                    label = prediction['class']
                    confidence = prediction['confidence']

                    # Hitung koordinat bounding box
                    x1 = x - width // 2
                    y1 = y - height // 2
                    x2 = x + width // 2
                    y2 = y + height // 2

                    # Dapatkan warna berdasarkan kelas dari kamus COLORS
                    color = COLORS.get(label, (255, 0, 0))  # Default ke biru jika kelas tidak ditemukan

                    # Gambar bounding box di gambar
                    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(image, f"{label} ({confidence:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Tampilkan gambar hasil deteksi
                cv2.imshow('Deteksi Objek', image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                # Simpan hasil gambar jika diperlukan
                result_image_path = os.path.join(result_folder, filename)
                cv2.imwrite(result_image_path, image)
                print(f"Hasil prediksi untuk {filename} berhasil disimpan di {result_image_path}")
            else:
                print(f"Error {response.status_code} untuk file {filename}: {response.text}")


