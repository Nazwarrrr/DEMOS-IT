import cv2
from cvzone.HandTrackingModule import HandDetector

# Buka kamera laptop
cap = cv2.VideoCapture(0)

# Inisialisasi detektor tangan
detector = HandDetector(detectionCon=0.7, maxHands=1)

# Nama jendela kamera
window_name = 'TikTok Trend Filter'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# Mulai dengan jendela kotak biasa (640x480)
is_fullscreen = False
cv2.resizeWindow(window_name, 640, 480)

print("Kontrol Keyboard:")
print("- Tekan 'Esc' untuk beralih antara Fullscreen dan Kotak Kecil Rata")
print("- Tekan 'q' untuk keluar")

# Variabel untuk transisi blur yang halus
current_blur = 1

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Balik frame biar kayak cermin
    frame = cv2.flip(frame, 1)
    
    # Deteksi tangan (draw=False biar polos tanpa skeleton)
    hands, frame = detector.findHands(frame, draw=False)

    is_peace = False

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        # Kondisi Peace
        if fingers == [0, 1, 1, 0, 0] or fingers == [1, 1, 1, 0, 0]:
            is_peace = True

    # Logika Transisi Animasi Blur
    if is_peace:
        if current_blur < 51:
            current_blur += 4
    else:
        if current_blur > 1:
            current_blur -= 4

    # Pastikan nilai blur ganjil
    blur_value = max(1, current_blur)
    if blur_value % 2 == 0:
        blur_value += 1

    # Terapkan blur jika filter aktif
    if blur_value > 1:
        frame = cv2.GaussianBlur(frame, (blur_value, blur_value), 0)
        
        # SEKARANG POLOS: Tanpa kotak hitam, tanpa watermark kanan
        # Hanya tulisan utama yang minimalis langsung di atas gambar
        cv2.putText(frame, "FOTO AKU BLURRRR.... :v", (20, 40), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

    # Tampilkan di layar
    cv2.imshow(window_name, frame)

    # Deteksi input keyboard
    key = cv2.waitKey(1) & 0xFF
    
    # Toggle Fullscreen vs Jendela Kotak Kecil Rata menggunakan 'Esc'
    if key == 27:
        is_fullscreen = not is_fullscreen
        
        if is_fullscreen:
            # Mode Fullscreen Layar Penuh
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        else:
            # Mode Kotak Kecil Sama Rata
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name, 640, 480) # Memaksa ukuran kembali ke kotak ideal

    # Keluar jika tekan 'q'
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()