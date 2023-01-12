
import json
import os


main_category='TTA_sample/IT'

json_list = []

for root, paths, files in os.walk(main_category) :
    for file in files :
        if os.path.splitext(os.path.join(root, file))[1] == '.json' :
            json_list.append(os.path.join(root, file))
            print(os.path.join(root, file))

# k = {}
# for i, j in enumerate(json_list) :
#     with open(j, "r") as f:
#         data = json.load(f)
#         k['a'][json_list[i]] = data

#print(k['TTA_sample/IT/H4131_스피커/스피커_Beosound_Balance/info.json'])

# print(data['data']) # list
# print('-'*100)

# h = data['data'][0]['Filename']
# print(h)





"""
하나의 아이템에 대한 조도별 다른 사진
RegisteredNumber을 키 값으로 하는 Value를 여러개 생성함

[{'ImageID': 'NW_2022_3010950760000_100_000_000_000_000', 'Filename': 'D:/TTA_sample/IT/H4131_스피커/스피커_Beosound_Balance/3010950760000/100_000_000_000_000.jpg', 
'AcquisitionMethod': '1', 'ProductID': '스피커', 'BrandCode': 'ZZ', 'ProductName': 'BALMUDA_The_Speaker', 'ClassCodeKR': 'H4131', 'ClassCodeINT': '14-01',
 'ViewPoint': 0, 'Angle': 0, 'Illuminance': '000', 'RegisteredNumber': '3010950760000', 'Packaging': '0'}, 
 
 {'ImageID': 'NW_2022_3010950760000_100_000_045_000_000', 'Filename': 'D:/TTA_sample/IT/H4131_스피커/스피커_Beosound_Balance/3010950760000/100_000_045_000_000.jpg', 
 'AcquisitionMethod': '1', 'ProductID': '스피커', 'BrandCode': 'ZZ','ProductName': 'BALMUDA_The_Speaker', 'ClassCodeKR': 'H4131', 'ClassCodeINT': '14-01', 
 'ViewPoint': 0, 'Angle': 45, 'Illuminance': '000', 'RegisteredNumber': '3010950760000', 'Packaging': '0'}, 
 
 {'ImageID': 'NW_2022_3010950760000_100_000_045_315_000', 'Filename': 'D:/TTA_sample/IT/H4131_스피커/스피커_Beosound_Balance/3010950760000/100_000_045_315_000.jpg', 
 'AcquisitionMethod': '1', 'ProductID': '스피커', 'BrandCode': 'ZZ', 'ProductName': 'BALMUDA_The_Speaker', 'ClassCodeKR': 'H4131', 'ClassCodeINT': '14-01', 
  'ViewPoint': 315, 'Angle': 45, 'Illuminance': '000', 'RegisteredNumber': '3010950760000', 'Packaging': '0'}]

ViewPoint, Angle, 
"""