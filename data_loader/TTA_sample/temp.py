import os
import json


def get_json(path, main_category, second_category_list, third_category_list):
    result = {}
    for i in range(len(second_category_list)): # 2
        image_id = []
        for j in range(len(third_category_list[i])):
            json_path = path + main_category + '/' + second_category_list[i] + '/' + third_category_list[i][j] + '/' + 'info.json'
            with open(json_path, 'r') as f:
                json_data = json.load(f)
                jsonArray =  json_data.get("data")
                for st in jsonArray:
                    image_id.append(st.get("ImageID"))
                                   
        result[second_category_list[i]] = image_id
    return result

def get_second_category(path, main_category):
    root_dir = os.path.join(path, main_category)
    root_under_dir_list = os.listdir(root_dir)
    return root_under_dir_list   # H4131_스피커, H4141_헤드폰


def get_third_category(path, main_category, second_category_list): # IT ,['H4131_스피커', 'H4141_헤드폰']
    
    third_catory_list = []
    for i in range(len(second_category_list)):
        root_dir = os.path.join(path+main_category,second_category_list[i]) # './ML_Tutorial/data_loader/TTA_sample/IT' + ['H4131_스피커', 'H4141_헤드폰']
        root_under_dir_list = os.listdir(root_dir) #  ['스피커_Beosound_Balance', '스피커_ANIMO', '스피커_AXIS_C1410_Network_Mini_Speaker'..]
        third_catory_list.append(root_under_dir_list)

    return third_catory_list



# 요기가 이제 main function 이지 않을까
path = './TTA_sample/'

main_category = 'test_item'

second_category_list = get_second_category(path, main_category)
'''
['H4131_스피커', 'H4141_헤드폰']
'''
third_category_list = get_third_category(path, main_category, second_category_list)
'''
[['스피커_Beosound_Balance', '스피커_ANIMO', '스피커_AXIS_C1410_Network_Mini_Speaker', '스피커_BEOSOUND_EMERGE', '스피커_BALMUDA_The_Speaker'], 
['헤드폰_AKG_K371_헤드폰', '헤드폰_AKG_K175_프로페셔널_접이식_밀폐형', '헤드폰_Awei_A790BL', '헤드폰_akg_headphone_y500bt', '헤드폰_Apple_에어팟_맥스']]
'''
image_ID = get_json(path, main_category, second_category_list, third_category_list)

result = {}
result[main_category] = image_ID
   
#print('H4131_스피커 개수 :', len(result['IT']['H4131_스피커']))
#print('H4141_헤드폰 개수 :', len(result['IT']['H4141_헤드폰']))

print(result)