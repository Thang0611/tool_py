from apkutils import APK
import os
import re
import xml.etree.ElementTree as ET
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
# def extract_manifest(apk_path, output_dir):
#     # Giải nén APK để lấy AndroidManifest.xml
#     subprocess.run(['apktool', 'd', apk_path, '-o', output_dir], check=True)
#     return os.path.join(output_dir, 'AndroidManifest.xml')

def parse_manifest(manifest_file):
    # Parse tệp XML
    tree = ET.parse(manifest_file)
    root = tree.getroot()

    # Lấy tên package từ thẻ gốc (root)
    package_name = root.attrib.get('package')

    # Danh sách để lưu thông tin activity
    activity_list = []

    # Duyệt qua các thẻ con và tìm thẻ <activity>
    for elem in root.iter('activity'):
        # Lấy giá trị của thuộc tính android:name
        activity_name = elem.attrib.get('{http://schemas.android.com/apk/res/android}name')
        # Kiểm tra thuộc tính android:exported
        exported = elem.attrib.get('{http://schemas.android.com/apk/res/android}exported')
        
        if activity_name and exported == 'true':
            # Thêm vào danh sách (package_name, activity_name)
            activity_list.append([package_name, activity_name])

    return activity_list

def save_to_csv(activity_list, output_file):
    # Chuyển dữ liệu sang DataFrame của pandas
    df = pd.DataFrame(activity_list, columns=['Package Name', 'Activity Class Name'])
    # Xuất dữ liệu ra file CSV
    df.to_csv(output_file, index=False)

def open_file_dialog():
    file_paths = filedialog.askopenfilenames(
        title="Select APK files",
        filetypes=[("APK files", "*.apk")]
    )
    if not file_paths:
        return
    print(file_paths)

    paths = []
    for file in file_paths:
        fileName = re.sub('.apk', '', file)
        print(file)
        print("-----------------------------------------------------------")
        print(f"Extracting AndroidManifest.xml of:: {fileName}")


        apk = APK.from_file(file).parse_resouce()
        xmlGenerated = apk.get_manifest()
        
        file_obj = open(f'{fileName}.xml', 'w')
        file_obj.write(xmlGenerated)
        file_obj.close()
        manifest_file=f'{fileName}.xml'
        tree = ET.parse(xmlGenerated)
        root = tree.getroot()

        package_name = root.attrib.get('package')

        activity_list = []

        for elem in root.iter('activity'):
        # Lấy giá trị của thuộc tính android:name
            activity_name = elem.attrib.get('{http://schemas.android.com/apk/res/android}name')
            exported = elem.attrib.get('{http://schemas.android.com/apk/res/android}exported')
            
            if activity_name and exported =="true":
                # Thêm vào danh sách (package_name, activity_name)
                activity_list.append([package_name, activity_name])
        df = pd.DataFrame(activity_list, columns=['Package Name', 'Activity Class Name'])

        # Xuất dữ liệu ra file Excel
        # output_file = 'activities.xlsx'
        # df.to_excel(output_file, index=False)
        output_file = f'C:/Users/NHT/Documents/file_CSV{fileName}.csv'
        df.to_csv(output_file, index=False)
        print(f"Extraction completed, {file_obj.name}")
        print("-----------------------------------------------------------")

# Tạo giao diện GUI
root = tk.Tk()
root.title("APK Activity Exporter")

button = tk.Button(root, text="Select APK Files", command=open_file_dialog)
button.pack(pady=20)

root.mainloop()
