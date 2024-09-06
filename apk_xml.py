from apkutils import APK
import os
import re
import xml.etree.ElementTree as ET
import pandas as pd

files = os.listdir("APKSamples/")
print(files)
paths = []
for file in files:
    filePath = f"APKSamples/{file}"
    fileName = re.sub('.apk', '', file)

    print("-----------------------------------------------------------")
    print(f"Extracting AndroidManifest.xml of:: {fileName}")


    apk = APK.from_file(filePath).parse_resouce()
    xmlGenerated = apk.get_manifest()
    
    file_obj = open(f'GeneratedXML/AndroidManifest-{fileName}.xml', 'w')
    file_obj.write(xmlGenerated)
    file_obj.close()
    manifest_file=f'GeneratedXML/AndroidManifest-{fileName}.xml'
    tree = ET.parse(manifest_file)
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
    output_file = f'{fileName}.csv'
    df.to_csv(output_file, index=False)
    print(f"Extraction completed, {file_obj.name}")
    print("-----------------------------------------------------------")

