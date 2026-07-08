import cv2
import time
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk

# ==========================================
# KONFIGURASI UKURAN HORIZONTAL (LANDSCAPE)
# ==========================================
LEBAR_KANVAS, TINGGI_KANVAS = 1200, 800
LEBAR_FOTO, TINGGI_FOTO = 460, 310

KOORDINAT_HORIZONTAL = [
    (100, 70),   # Kotak 1
    (640, 70),   # Kotak 2
    (100, 410),  # Kotak 3
    (640, 410)   # Kotak 4
]

class PhotoboothApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Mini Photobooth Fullscreen Pro")
        
        # JENDELA OTOMATIS FULLSCREEN
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#0f0f14")
        
        # Bind tombol ESC agar bisa keluar dari fullscreen
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        self.cap = None
        self.foto_tersimpan = []
        self.total_foto = 4
        self.durasi_countdown = 4
        self.jenis_tema = ""
        
        # Container utama fullscreen
        self.main_frame = tk.Frame(self.root, bg="#0f0f14")
        self.main_frame.pack(expand=True, fill="both")
        
        # Mulai Aplikasi
        self.tampilkan_menu_utama()

    # ==========================================
    # FUNGSI MEMBUAT TEMPLATE HORIZONTAL OTOMATIS
    # ==========================================
    def buat_template_horizontal(self, jenis_tema):
        canvas = Image.new("RGB", (LEBAR_KANVAS, TINGGI_KANVAS), "white")
        draw = ImageDraw.Draw(canvas)
        
        if jenis_tema == "arcade":
            canvas.paste((15, 15, 25), [0, 0, LEBAR_KANVAS, TINGGI_KANVAS])
            for x in range(0, LEBAR_KANVAS, 80): draw.line([(x, 0), (x, TINGGI_KANVAS)], fill=(30, 30, 60), width=1)
            for y in range(0, TINGGI_KANVAS, 80): draw.line([(0, y), (LEBAR_KANVAS, y)], fill=(30, 30, 60), width=1)
            draw.rectangle([(20, 20), (LEBAR_KANVAS-20, TINGGI_KANVAS-20)], outline=(0, 240, 255), width=6)
            for box in KOORDINAT_HORIZONTAL:
                x, y = box
                draw.rectangle([(x, y), (x + LEBAR_FOTO, y + TINGGI_FOTO)], fill=(40, 40, 50), outline=(255, 0, 128), width=4)
            draw.text((LEBAR_KANVAS // 2, TINGGI_KANVAS - 45), "⚡ RETRO ARCADE PHOTOBOOTH ⚡", fill=(0, 240, 255), anchor="mm")
            
        elif jenis_tema == "vintage":
            canvas.paste((245, 235, 215), [0, 0, LEBAR_KANVAS, TINGGI_KANVAS])
            draw.rectangle([(20, 20), (LEBAR_KANVAS-20, TINGGI_KANVAS-20)], outline=(90, 50, 30), width=5)
            draw.rectangle([(30, 30), (LEBAR_KANVAS-30, TINGGI_KANVAS-30)], outline=(255, 255, 255), width=2)
            for box in KOORDINAT_HORIZONTAL:
                x, y = box
                draw.rectangle([(x, y), (x + LEBAR_FOTO, y + TINGGI_FOTO)], fill=(225, 215, 195), outline=(120, 70, 40), width=4)
            draw.text((LEBAR_KANVAS // 2, TINGGI_KANVAS - 45), "✨ GOOD TIMES & MEMORIES ✨", fill=(90, 50, 30), anchor="mm")
            
        return canvas

    # ==========================================
    # HALAMAN 1: MENU UTAMA + PREVIEW GRAFIK
    # ==========================================
    def tampilkan_menu_utama(self):
        self.bersihkan_frame()
        
        # Judul Besar Fullscreen
        label_judul = tk.Label(self.main_frame, text="📸 SCREEN CAPTURE STUDIO 📸", 
                               font=("Helvetica", 32, "bold"), bg="#0f0f14", fg="#ffffff")
        label_judul.pack(pady=(60, 10))

        label_sub = tk.Label(self.main_frame, text="PILIH TEMPLATE CETAKAN DI BAWAH INI UNTUK MEMULAI KAMERA:", 
                             font=("Helvetica", 14, "bold"), bg="#0f0f14", fg="#00ffcc")
        label_sub.pack(pady=10)

        # Frame Kontainer Pilihan Kiri & Kanan (Dibuat Gede)
        frame_pilihan = tk.Frame(self.main_frame, bg="#0f0f14")
        frame_pilihan.pack(pady=40, expand=True)

        # --- GENERATE LIVE PREVIEW GRAFIK UNTUK TOMBOL ---
        # 1. Preview Arcade (Ukuran ciut untuk preview: 450x300 px)
        preview_arcade_img = self.buat_template_horizontal("arcade").resize((450, 300))
        self.img_arcade_tk = ImageTk.PhotoImage(image=preview_arcade_img)
        
        # 2. Preview Vintage
        preview_vintage_img = self.buat_template_horizontal("vintage").resize((450, 300))
        self.img_vintage_tk = ImageTk.PhotoImage(image=preview_vintage_img)

        # --- SEKSI PILIHAN KIRI: ARCADE ---
        frame_kiri = tk.Frame(frame_pilihan, bg="#0f0f14")
        frame_kiri.grid(row=0, column=0, padx=50)
        
        # Menggunakan gambar preview asli sebagai tombol klik
        btn_img_arcade = tk.Button(frame_kiri, image=self.img_arcade_tk, bd=4, relief="ridge",
                                   cursor="hand2", command=lambda: self.mulai_photobooth("arcade"))
        btn_img_arcade.pack()
        
        label_arcade = tk.Label(frame_kiri, text="🕹️ RETRO ARCADE STYLE", font=("Arial", 16, "bold"), 
                                bg="#0f0f14", fg="#ff007f")
        label_arcade.pack(pady=15)

        # --- SEKSI PILIHAN KANAN: VINTAGE ---
        frame_kanan = tk.Frame(frame_pilihan, bg="#0f0f14")
        frame_kanan.grid(row=0, column=1, padx=50)
        
        btn_img_vintage = tk.Button(frame_kanan, image=self.img_vintage_tk, bd=4, relief="ridge",
                                    cursor="hand2", command=lambda: self.mulai_photobooth("vintage"))
        btn_img_vintage.pack()
        
        label_vintage = tk.Label(frame_kanan, text="🧸 VINTAGE MEMORIES STYLE", font=("Arial", 16, "bold"), 
                                 bg="#0f0f14", fg="#f39c12")
        label_vintage.pack(pady=15)
        
        # Tombol Keluar di Bawah
        btn_keluar = tk.Button(self.main_frame, text="KELUAR APLIKASI (ESC)", font=("Arial", 12, "bold"),
                               bg="#ff3333", fg="white", bd=2, command=self.root.quit, padx=20, pady=5)
        btn_keluar.pack(side="bottom", pady=40)

    # ==========================================
    # HALAMAN 2: LAYAR KAMERA & COUNTDOWN
    # ==========================================
    def mulai_photobooth(self, tema):
        self.jenis_tema = tema
        self.bersihkan_frame()
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Webcam tidak terdeteksi!")
            self.tampilkan_menu_utama()
            return
            
        self.foto_tersimpan = []
        
        self.label_info = tk.Label(self.main_frame, text="SIAP-SIAP GAYA! TEKAN [SPASI] UNTUK MULAI", 
                                   font=("Helvetica", 24, "bold"), bg="#0f0f14", fg="#00ffcc")
        self.label_info.pack(pady=30)
        
        # Kamera dibuat besar biar puas pas ngeliat fullscreen (880x660 px)
        self.canvas_cam = tk.Label(self.main_frame, bg="black", bd=6, relief="solid")
        self.canvas_cam.pack(pady=10)
        
        self.mulai_foto = False
        self.hitung_foto = 0
        self.waktu_mulai = 0
        
        self.root.bind("<space>", self.pemicu_tombol_spasi)
        self.update_kamera()

    def pemicu_tombol_spasi(self, event):
        if not self.mulai_foto:
            self.mulai_foto = True
            self.waktu_mulai = time.time()
            self.root.unbind("<space>")

    def update_kamera(self):
        if self.cap is None: return
        
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame_resized = cv2.resize(frame, (880, 660))
            tinggi, lebar, _ = frame_resized.shape
            
            if self.mulai_foto:
                waktu_sisa = int(self.durasi_countdown - (time.time() - self.waktu_mulai))
                
                if waktu_sisa > 0:
                    self.label_info.config(text=f"POSE UNTUK FOTO KE {self.hitung_foto + 1} / 4", fg="#ff007f")
                    cv2.putText(frame_resized, str(waktu_sisa), (lebar // 2 - 35, tinggi // 2 + 40), 
                                cv2.FONT_HERSHEY_DUPLEX, 5, (0, 255, 255), 7)
                else:
                    nama_file = f"temp_{self.hitung_foto + 1}_{int(time.time())}.jpg"
                    cv2.imwrite(nama_file, frame)
                    self.foto_tersimpan.append(nama_file)
                    
                    self.hitung_foto += 1
                    self.waktu_mulai = time.time()
                    
                    if self.hitung_foto >= self.total_foto:
                        self.cap.release()
                        self.cap = None
                        self.proses_kolase()
                        return
            
            cv2image = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas_cam.imgtk = imgtk
            self.canvas_cam.configure(image=imgtk)
            
        self.root.after(15, self.update_kamera)

    # ==========================================
    # HALAMAN 3: TAMPILKAN HASIL AKHIR
    # ==========================================
    def proses_kolase(self):
        self.bersihkan_frame()
        
        canvas_template = self.buat_template_horizontal(self.jenis_tema)

        for i, file_foto in enumerate(self.foto_tersimpan):
            if os.path.exists(file_foto):
                img = Image.open(file_foto)
                img = img.resize((LEBAR_FOTO, TINGGI_FOTO))
                canvas_template.paste(img, KOORDINAT_HORIZONTAL[i])
                os.remove(file_foto)

        nama_hasil = f"hasil_photobooth_{self.jenis_tema}_{int(time.time())}.jpg"
        canvas_template.save(nama_hasil)

        label_sukses = tk.Label(self.main_frame, text="🎉 BERHASIL DICETAK & DISIMPAN! 🎉", 
                                font=("Helvetica", 24, "bold"), bg="#0f0f14", fg="#00ff00")
        label_sukses.pack(pady=20)

        # Hasil kolase ditampilkan besar (960x640 px) biar pas fullscreen
        img_display = canvas_template.resize((960, 640))
        imgtk = ImageTk.PhotoImage(image=img_display)
        
        label_hasil = tk.Label(self.main_frame, image=imgtk, bg="#0f0f14", bd=4, relief="solid")
        label_hasil.image = imgtk
        label_hasil.pack(pady=5)

        btn_back = tk.Button(self.main_frame, text="CETAK FOTO BARU (KEMBALI)", font=("Arial", 16, "bold"),
                             bg="#2ecc71", fg="white", width=25, height=2, bd=3, cursor="hand2",
                             command=self.tampilkan_menu_utama)
        btn_back.pack(pady=25)

    def bersihkan_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        if self.cap is not None:
            self.cap.release()
            self.cap = None

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoboothApp(root)
    root.mainloop()