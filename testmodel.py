import cv2
import time

video = cv2.VideoCapture(0)

facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Pastikan OpenCV-contrib-python terinstal untuk modul face
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("Trainer.yml")

name_list = ["", "Jean", "Hugo", "Lovina"]

# Waktu mulai untuk deteksi
start_time = time.time()

# Variabel untuk menyimpan nama yang terdeteksi
detected_names = []

while True:
    ret, frame = video.read()
    if not ret:
        print("Tidak dapat membaca frame dari kamera.")
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        serial, conf = recognizer.predict(gray[y:y+h, x:x+w])
        print(f"Serial: {serial}, Confidence: {conf}")
        if conf < 50:  # Ubah logika ambang batas
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            name = name_list[serial]
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            if name not in detected_names:
                detected_names.append(name)
        else:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    frame = cv2.resize(frame, (640, 480))
    cv2.imshow("Face Recognition", frame)

    # Periksa apakah waktu telah mencapai 10 detik
    if time.time() - start_time > 10:
        print("Verifikasi selesai, menunggu hasil....")
        break  # Hentikan loop setelah 10 detik

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Menutup video capture dan jendela setelah 10 detik
video.release()
cv2.destroyAllWindows()

# Menampilkan hasil nama yang terdeteksi
if detected_names:
    print("Wajah yang terdeteksi dalam 10 detik:")
    for name in detected_names:
        print(name)
else:
    print("Tidak ada wajah yang terdeteksi dalam 10 detik.")
