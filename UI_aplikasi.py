import os
import subprocess
import tkinter as tk
from tkinter import messagebox

# Variabel untuk menyimpan hasil verifikasi
hasil_verifikasi = {
    "confidence": None,
    "tipe_verifikasi": None
}

# Fungsi untuk menjalankan file eksternal
def jalankan_file(file_name):
    try:
        # Dapatkan path direktori utama tempat file utama berada
        folder_path = os.path.dirname(__file__)
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith(".py"):
            subprocess.run(["python", file_path], check=True)
        elif file_name.endswith(".exe"):
            subprocess.run([file_path], check=True)
        return True
    except Exception as e:
        return f"Error: {e}"

# Window 2 (Verifikasi)
def tombol2_window2():
    file_name = "testingsuara.py"  # Ganti dengan nama file Python
    result = jalankan_file(file_name)
    if result is True:
        teks2_label.config(text="Terverifikasi!")
        # Menampilkan tombol "Next Window" setelah verifikasi selesai
        next_window_btn.pack(pady=10)
        cek_verifikasi()
    else:
        teks2_label.config(text=result)

# Fungsi untuk tombol di Window 3
def tombol1_window3():
    file_name = "testmodel.py"  # Ganti dengan nama file Python
    result = jalankan_file(file_name)
    if result is True:
        teks1_label.config(text="Terverifikasi!")
        # Menampilkan tombol "Kembali ke Home" setelah verifikasi selesai
        kembali_btn3.pack(pady=10)  # Tampilkan tombol "Kembali ke Home"
        cek_verifikasi()
    else:
        teks1_label.config(text=result)


# Fungsi untuk memeriksa verifikasi di Window 2
def cek_verifikasi():
    if teks1_label.cget("text") == "Tombol 1 diverifikasi!" and teks2_label.cget("text") == "Tombol 2 diverifikasi!":
        messagebox.showinfo("Info", "Verifikasi selesai!")
        buka_window3()

# Fungsi untuk membuka Window 3 setelah verifikasi selesai
def buka_window3():
    window2.withdraw()  # Sembunyikan Window 2
    window3.deiconify()  # Tampilkan Window 3

# Fungsi untuk membuka Window 4 untuk input dataset
def buka_window4():
    window1.withdraw()  # Sembunyikan Window 1
    window4.deiconify()  # Tampilkan Window 4

# Fungsi untuk tombol di Window 4
def tombol1_window4():
    file_name = "datacollect.py"  # Ganti dengan nama file Python
    result = jalankan_file(file_name)
    if result is True:
        teks1_dataset.config(text="Training selesai untuk Dataset Foto")
    else:
        teks1_dataset.config(text=result)

# Fungsi untuk kembali ke Window 1 dan memulai ulang seluruh aplikasi
def kembali_ke_window1(current_window):
    current_window.withdraw()  # Sembunyikan jendela saat ini
    window1.deiconify()  # Tampilkan Window 1
    
    # Reset status hasil verifikasi
    hasil_verifikasi["confidence"] = None
    hasil_verifikasi["tipe_verifikasi"] = None
    
    # Reset teks dan status lainnya jika diperlukan
    teks2_label.config(text="Sedang Cek...")
    teks1_label.config(text="Sedang Cek...")
    teks1_dataset.config(text="Training...")
    
    # Sembunyikan tombol Next Window di awal
    next_window_btn.pack_forget()

    # Menyembunyikan Window 2, 3, 4
    window2.withdraw()
    window3.withdraw()
    window4.withdraw()

    # Sembunyikan tombol "Kembali ke Home" setelah kembali ke Window 1
    kembali_btn3.pack_forget()  # Sembunyikan tombol "Kembali ke Home"


# Fungsi untuk menutup semua window
def tutup_semua_window():
    window1.destroy()
    window2.destroy()
    window3.destroy()
    window4.destroy()

# Membuat Window 1
window1 = tk.Tk()
window1.title("Home")
window1.geometry("300x400")

label1 = tk.Label(window1, text="STOP! Verifikasi dahulu", font=("Arial", 14))
label1.pack(pady=20)

verifikasi_btn = tk.Button(window1, text="Verifikasi", command=lambda: [window1.withdraw(), window2.deiconify()], bg="red", fg="white")
verifikasi_btn.pack(pady=10)

dataset_btn = tk.Button(window1, text="Training ", command=buka_window4, bg="blue", fg="white")
dataset_btn.pack(pady=10)

tutup_btn = tk.Button(window1, text="Tutup Semua Window", command=tutup_semua_window, bg="gray", fg="white")
tutup_btn.pack(pady=10)

# Membuat Window 2
window2 = tk.Toplevel()
window2.title("Verifikasi Suara")
window2.geometry("300x400")
window2.withdraw()

label2 = tk.Label(window2, text="Verifikasi Suara", font=("Arial", 14))
label2.pack(pady=20)

btn2 = tk.Button(window2, text="Verifikasi", command=tombol2_window2)
btn2.pack(pady=10)
teks2_label = tk.Label(window2, text="Sedang Cek...")
teks2_label.pack(pady=5)

# Tombol Next Window yang disembunyikan di awal
next_window_btn = tk.Button(window2, text="Berikutnya", command=buka_window3)
next_window_btn.pack_forget()  # Tombol ini disembunyikan pada awal

# Membuat Window 3
window3 = tk.Toplevel()
window3.title("Verifikasi Wajah")
window3.geometry("300x400")
window3.withdraw()

# Label Verifikasi Wajah
label_verifikasi = tk.Label(window3, text="Verifikasi Wajah", font=("Arial", 14))
label_verifikasi.pack(pady=10)

# Tombol Verifikasi Wajah
btn_verifikasi = tk.Button(window3, text="Verifikasi", command=tombol1_window3)
btn_verifikasi.pack(pady=10)

# Label "Sedang Cek..."
teks1_label = tk.Label(window3, text="Sedang Cek...")
teks1_label.pack(pady=5)

# Tombol "Kembali ke Window 1"
kembali_btn3 = tk.Button(window3, text="Kembali ke Home", command=lambda: kembali_ke_window1(window3))
kembali_btn3.pack(pady=10)

# Membuat Window 4
window4 = tk.Toplevel()
window4.title("Dataset")
window4.geometry("300x400")
window4.withdraw()

label4 = tk.Label(window4, text="Dataset", font=("Arial", 14))
label4.pack(pady=20)

btn1_dataset = tk.Button(window4, text="Training Dataset Foto", command=tombol1_window4)
btn1_dataset.pack(pady=10)
teks1_dataset = tk.Label(window4, text="Training...")
teks1_dataset.pack(pady=5)

kembali_btn4 = tk.Button(window4, text="Kembali ke Window 1", command=lambda: kembali_ke_window1(window4))
kembali_btn4.pack(pady=10)

# Menjalankan aplikasi
window1.mainloop()
