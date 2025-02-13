# import streamlit as st
# from ultralytics import YOLO
# import cv2
# import numpy as np
# import tempfile
# import time
# from scipy.spatial import distance
# import firebase_admin
# from firebase_admin import credentials, db

# # Inisialisasi Firebase (gunakan file JSON kredensial Anda)
# if not firebase_admin._apps:
#     cred = credentials.Certificate("credentials.json")
#     firebase_admin.initialize_app(cred, {
#         'databaseURL': 'https://parking-detection-34614-default-rtdb.asia-southeast1.firebasedatabase.app/'
#     })

# # Memuat model YOLOv8
# model = YOLO('lasttrain.pt')

# # Mengatur konfigurasi halaman Streamlit
# st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# # Pengaturan sidebar
# st.sidebar.header('Deteksi Area Parkir oleh: JKAS')

# # Pengaturan Confidence dan IOU
# confidence = st.sidebar.slider("Ambang Batas Confidence", 0.0, 1.0, 0.5)
# iou_threshold = st.sidebar.slider("Ambang Batas IOU", 0.0, 1.0, 0.5)

# # Pengaturan checkbox untuk menampilkan label dan ID
# show_labels = st.sidebar.checkbox("Tampilkan Label", True)
# show_ids = st.sidebar.checkbox("Tampilkan ID", True)

# # Penyimpanan ID slot dan posisinya
# slot_positions = {}
# base_letter = 'A'
# id_counter = 1

# # Fungsi untuk menetapkan ID yang konsisten untuk setiap slot parkir
# def assign_slot_id(x1, y1, x2, y2, threshold=50):
#     global id_counter
#     box_center = ((x1 + x2) // 2, (y1 + y2) // 2)
#     closest_id = None
#     closest_distance = float('inf')
    
#     for slot_id, pos in slot_positions.items():
#         dist = distance.euclidean(box_center, pos)
#         if dist < closest_distance and dist < threshold:
#             closest_distance = dist
#             closest_id = slot_id
    
#     if closest_id is None:
#         # Menetapkan ID baru jika tidak ada slot yang cukup dekat
#         closest_id = f"{base_letter}{id_counter}"
#         slot_positions[closest_id] = box_center
#         id_counter += 1
#     else:
#         # Memperbarui posisi untuk slot yang sudah ada
#         slot_positions[closest_id] = box_center
    
#     return closest_id

# # Fungsi untuk mendeteksi objek pada gambar menggunakan YOLOv8
# def detect_objects(image, conf_threshold, iou_threshold):
#     results = model(image, conf=conf_threshold, iou=iou_threshold)
#     return results

# # Fungsi untuk menggambar kotak pembatas dan menghitung slot parkir
# def draw_boxes(image, results):
#     num_free_slots = 0
#     num_occupied_slots = 0
#     empty_slots = []  # List untuk menyimpan ID slot yang kosong
    
#     for result in results:
#         for box in result.boxes:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             confidence = box.conf[0]
#             class_id = int(box.cls[0])
#             slot_id = assign_slot_id(x1, y1, x2, y2)
            
#             # Menghitung slot kosong dan terisi
#             if model.names[class_id] == "free":
#                 num_free_slots += 1
#                 empty_slots.append(slot_id)  # Tambahkan ID slot kosong ke list
#                 label_color = (0, 255, 0)  # Hijau untuk slot kosong
#             elif model.names[class_id] == "car":
#                 num_occupied_slots += 1
#                 label_color = (0, 0, 255)  # Merah untuk mobil
            
#             if show_labels:
#                 label = f"{model.names[class_id]} {confidence:.2f}"
#                 cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, label_color, 1)
                
#             if show_ids:
#                 id_label = f"ID:{slot_id}"
#                 cv2.putText(image, id_label, (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, label_color, 1)

#             cv2.rectangle(image, (x1, y1), (x2, y2), label_color, 2)

#     # Menampilkan total slot, jumlah kosong, dan terisi
#     total_slots = num_free_slots + num_occupied_slots
#     parking_summary = f"Total: {total_slots} Kosong: {num_free_slots} Mobil: {num_occupied_slots}"
#     cv2.putText(image, parking_summary, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#     return image, num_free_slots, num_occupied_slots, empty_slots

# # Fungsi untuk memperbarui data parkir di Firebase
# def update_parking_data(num_free_slots, num_occupied_slots):
#     ref = db.reference('parking')
#     ref.set({
#         'num_free_slots': num_free_slots,
#         'num_occupied_slots': num_occupied_slots
#     })

# # Fungsi untuk mengakses kamera dan melakukan deteksi secara live
# def live_camera_feed():
#     camera_index = 0  # Menggunakan kamera default
#     video_cap = cv2.VideoCapture(camera_index)
#     stframe = st.empty()
#     warning_placeholder = st.empty()  # Tempat untuk menampilkan status slot kosong atau penuh

#     while video_cap.isOpened():
#         ret, frame = video_cap.read()
#         if not ret:
#             st.error("Tidak dapat mengakses kamera.")
#             break
        
#         # Melakukan deteksi di setiap frame
#         results = detect_objects(frame, confidence, iou_threshold)
#         frame, num_free_slots, num_occupied_slots, empty_slots = draw_boxes(frame, results)

#         # Tampilkan frame hasil deteksi
#         stframe.image(frame, channels="BGR", use_column_width=True)

#         # Tampilkan status parkir
#         if num_free_slots == 0:
#             warning_placeholder.warning("Parkir Penuh")
#         else:
#             empty_slots_str = ", ".join(empty_slots)
#             warning_placeholder.success(f"Slot Kosong: {empty_slots_str}")
        
#         # Update data di Firebase
#         update_parking_data(num_free_slots, num_occupied_slots)

#     video_cap.release()

# # Menampilkan opsi untuk menggunakan kamera langsung
# st.sidebar.subheader("Input melalui kamera")
# if st.sidebar.button("Mulai Kamera"):
#     live_camera_feed()


import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
from scipy.spatial import distance
import firebase_admin
from firebase_admin import credentials, db

# Inisialisasi Firebase (gunakan file JSON kredensial Anda)
if not firebase_admin._apps:
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://parking-detection-34614-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Memuat model YOLOv8
model = YOLO('lasttrain.pt')

# Sidebar dan pengaturan konfigurasi
st.sidebar.header('Deteksi Area Parkir oleh: JKAS')
confidence = st.sidebar.slider("Ambang Batas Confidence", 0.0, 1.0, 0.5)
iou_threshold = st.sidebar.slider("Ambang Batas IOU", 0.0, 1.0, 0.5)

show_labels = st.sidebar.checkbox("Tampilkan Label", True)
show_ids = st.sidebar.checkbox("Tampilkan ID", True)

slot_positions = {}
base_letter = 'A'
id_counter = 1

def assign_slot_id(x1, y1, x2, y2, threshold=50):
    global id_counter
    box_center = ((x1 + x2) // 2, (y1 + y2) // 2)
    closest_id = None
    closest_distance = float('inf')
    
    for slot_id, pos in slot_positions.items():
        dist = distance.euclidean(box_center, pos)
        if dist < closest_distance and dist < threshold:
            closest_distance = dist
            closest_id = slot_id
    
    if closest_id is None:
        closest_id = f"{base_letter}{id_counter}"
        slot_positions[closest_id] = box_center
        id_counter += 1
    else:
        slot_positions[closest_id] = box_center
    
    return closest_id

def detect_objects(image, conf_threshold, iou_threshold):
    results = model(image, conf=conf_threshold, iou=iou_threshold)
    return results

def draw_boxes(image, results):
    num_free_slots = 0
    num_occupied_slots = 0
    empty_slots = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf[0]
            class_id = int(box.cls[0])
            slot_id = assign_slot_id(x1, y1, x2, y2)
            
            if model.names[class_id] == "free":
                num_free_slots += 1
                empty_slots.append(slot_id)
                label_color = (0, 255, 0)
            elif model.names[class_id] == "car":
                num_occupied_slots += 1
                label_color = (0, 0, 255)
            
            if show_labels:
                label = f"{model.names[class_id]} {confidence:.2f}"
                cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, label_color, 1)
                
            if show_ids:
                id_label = f"ID:{slot_id}"
                cv2.putText(image, id_label, (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, label_color, 1)

            cv2.rectangle(image, (x1, y1), (x2, y2), label_color, 2)

    total_slots = num_free_slots + num_occupied_slots
    parking_summary = f"Total: {total_slots} Kosong: {num_free_slots} Mobil: {num_occupied_slots}"
    cv2.putText(image, parking_summary, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return image, num_free_slots, num_occupied_slots, empty_slots

def update_parking_data(num_free_slots, num_occupied_slots):
    ref = db.reference('parking')
    ref.set({
        'num_free_slots': num_free_slots,
        'num_occupied_slots': num_occupied_slots
    })

def live_camera_feed():
    camera_index = 0
    video_cap = cv2.VideoCapture(camera_index)
    stframe = st.empty()
    warning_placeholder = st.empty()

    while video_cap.isOpened():
        ret, frame = video_cap.read()
        if not ret:
            st.error("Tidak dapat mengakses kamera.")
            break
        
        results = detect_objects(frame, confidence, iou_threshold)
        frame, num_free_slots, num_occupied_slots, empty_slots = draw_boxes(frame, results)

        stframe.image(frame, channels="BGR", use_column_width=True)

        if num_free_slots == 0:
            warning_placeholder.warning("Parkir Penuh")
        else:
            empty_slots_str = ", ".join(empty_slots)
            warning_placeholder.success(f"Slot Kosong: {empty_slots_str}")
        
        update_parking_data(num_free_slots, num_occupied_slots)

    video_cap.release()

st.sidebar.subheader("Input melalui kamera")
if st.sidebar.button("Mulai Kamera"):
    live_camera_feed()
