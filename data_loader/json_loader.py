import json
import os
import random

class CustomDataLoader() :
    def __init__(self, main_path : str, want_items : list = None, option=None) :
        
        self.main_path = main_path
        self.product_json_list = self.get_product_json_list(self.main_path) # main_path로 부터 json파일 경로를 전부 로드
        self.item_list = self.get_item_list_from_json(self.product_json_list) # 모든 json파일을 로드해서 가지고 있음(key값은 product_json_list)
        self.random_seed = 42
        
        if want_items is not None :
            self.get_item(want_items)

        self.ImageID = {}
        self.Filename = {} 
        self.AcquisitionMethod = {}
        self.ProductID = {}
        self.BrandCode = {}
        self.ProductName = {}
        self.ClassCodeKR = {}
        self.ClassCodeINT= {}
        self.ViewPoint = {}
        self.Angle = {}
        self.Illuminance = {}
        self.RegisteredNumber = {}
        self.Packaging = {}

        self.append_json_value(self.product_json_list, self.item_list)


    def append_json_value(self, json_lists, data) :


        d = {}
        d['IT'] = {}
        d['IT']['A'] = ['1', '2']
        d['IT']['B'] = ['3', '4']


        #for json_list in json_lists :
       
        json_list = 'TTA_sample/IT/H4131_스피커/스피커_Beosound_Balance/info.json'


        first_category = json_list.split('/')[1]
        second_category = json_list.split('/')[2]
        temp = second_category

        a = []

        for i in range(len(data[json_list]['data'])) :
            a.append(data[json_list]['data'][i]['ImageID'])


        print(a)


        #print(first_category, second_category)
        # self.ImageID[first_category] = {}
        # self.ImageID[first_category][second_category] = [[data[json_list]['data'][i]['ImageID']] for i in range(len(data[json_list]['data']))]


        # json_list = 'TTA_sample/IT/H4131_스피커/스피커_ANIMO/info.json'
        # first_category = json_list.split('/')[1]
        # second_category = json_list.split('/')[2]

        #print(first_category, second_category)
        #self.ImageID[first_category] = {}
        #self.ImageID[first_category][second_category] = [[data[json_list]['data'][i]['ImageID']] for i in range(len(data[json_list]['data']))]



        #self.ImageID[first_category] = {second_category : [data[json_list]['data'][i]['ImageID'] for i in range(len(data[json_list]['data']))]}
        #for json_list in json_lists :
        #num = len(data[json_list]['data']) # 3
        #self.ImageID[]

        # for i in range(len(data[json_list]['data'])) :
        #     first_category = data[json_list]['data'][i]['Filename'].split('/')[2] # IT(대분류)
        #     second_category = data[json_list]['data'][i]['Filename'].split('/')[3] # H4131(소분류)
        #print(data[json_list]['data'][i]['ImageID'])
            #self.ImageID[first_category] = {second_category : [data[json_list]['data'][i]['ImageID']]}
            #self.ImageID[second_category] = {second_category : [data[json_list]['data'][i]['ImageID']]}
            #self.ImageID[first_category] = {second_category : [data[json_list]['data'][i]['ImageID']]}
            #self.ImageID[first_category] = second_category
            #self.ImageID[first_category][second_category] = [data[json_list]['data'][i]['ImageID']]
            # num = len(data[json_list]['data'])
            # for i in range(num) :
            #     self.ImageID[first_category] = [second_category]
        print(self.ImageID)
        # self.ImageID[second_category] = [data[json_list]['data'][i]['ImageID'] for i in range(num)]
        #print(self.ImageID['IT']['H4131_스피커'])

        # json_list = 'TTA_sample/IT/H4131_스피커/스피커_ANIMO/info.json'
        # first_category = json_list.split('/')[1] # IT(대분류)
        # second_category = json_list.split('/')[2] # H4131(소분류)

        # num = len(data[json_list]['data'])
        # self.ImageID[first_category] = second_category
        # self.ImageID[second_category] = [data[json_list]['data'][i]['ImageID'] for i in range(num)]
        

        # json_list = 'TTA_sample/IT/H4141_헤드폰/헤드폰_AKG_K371_헤드폰/info.json'
        # first_category = json_list.split('/')[1] # IT(대분류)
        # second_category = json_list.split('/')[2] # H4131(소분류)

        # num = len(data[json_list]['data'])
        # self.ImageID[first_category] = second_category
        # self.ImageID[second_category] = [data[json_list]['data'][i]['ImageID'] for i in range(num)]

        #print(self.ImageID)

            #print(first_category, second_category)
        #     num = len(data[json_list]['data'])
            
        #     #self.ImageID[json_list] = [{i:data[json_list]['data'][i]['ImageID']} for i in range(num)]

        #     first_category = json_list.split('/')[1] # IT(대분류)
        #     second_category = json_list.split('/')[2] # H4131(소분류)
        #     print(second_category)
        #     #if counter == True :
        #     self.ImageID[first_category] = second_category
        #      #   counter = False
        #     self.ImageID[second_category] = [data[json_list]['data'][i]['ImageID'] for i in range(num)]
        # print(self.ImageID)


            # self.Filename[json_list] = [{i:data[json_list]['data'][i]['Filename']} for i in range(num)]
            # self.AcquisitionMethod[json_list] = [{i:data[json_list]['data'][i]['AcquisitionMethod']} for i in range(num)]
            # self.ProductID[json_list] = [{i:data[json_list]['data'][i]['ProductID']} for i in range(num)]
            # self.BrandCode[json_list] = [{i:data[json_list]['data'][i]['BrandCode']} for i in range(num)]
            # self.ProductName[json_list] = [{i:data[json_list]['data'][i]['ProductName']} for i in range(num)]
            # self.ClassCodeKR[json_list] = [{i:data[json_list]['data'][i]['ClassCodeKR']} for i in range(num)]
            # self.ClassCodeINT[json_list] = [{i:data[json_list]['data'][i]['ClassCodeINT']} for i in range(num)]
            # self.ViewPoint[json_list] = [{i:data[json_list]['data'][i]['ViewPoint']} for i in range(num)]
            # self.Angle[json_list] = [{i:data[json_list]['data'][i]['Angle']} for i in range(num)]
            # self.Illuminance[json_list] = [{i:data[json_list]['data'][i]['Illuminance']} for i in range(num)]
            # self.RegisteredNumber[json_list] = [{i:data[json_list]['data'][i]['RegisteredNumber']} for i in range(num)]
            # self.Packaging[json_list] = [{i:data[json_list]['data'][i]['Packaging']} for i in range(num)]

        
        #print(self.ImageID)


    def get_item_list_from_json(self, json_list) :
        all_json = {}
        for i, j in enumerate(json_list) :
            with open(j, "r") as f:
                data = json.load(f)
                all_json[json_list[i]] = data

        return all_json

    def get_product_json_list(self, main_path) :
        json_list = []
        for root, paths, files in os.walk(main_path) :
            for file in files :
                if os.path.splitext(os.path.join(root, file))[1] == '.json' :
                    json_list.append(os.path.join(root, file))

        #print(json_list)
        print(f'number of json file: {len(json_list)}')
        return json_list



    def get_item(self, want_items) :
        #want_item_list = []
        #for want_item in want_items :
        want_items = 3
        if want_item == "ImageID":
            #want_item_list.append(self.ImageID)
            print(0)
        elif want_item == "Filename":
            print (1)
        elif want_item == "AcquisitionMethod":
            print (2)
        elif want_item == "ProductID":
            print (3)
        elif want_item == "BrandCode":
            print (4)
        elif want_item == "ProductName":
            print (5)
        elif want_item == "ClassCodeKR":
            print (6)
        elif want_item == "ClassCodeINT":
            print (7)
        elif want_item == "ViewPoint":
            print (8)
        elif want_item == "Angle":
            print (9)
        elif want_item == "Illuminance":
            print (10)
        elif want_item == "RegisteredNumber":
            print (11)
        elif want_item == "Packaging":
            print (12)
            
            
    def get_train_test_split() :
        pass


main_category='TTA_sample/IT'

CustomDataLoader(main_category)







# https://jimmy-ai.tistory.com/147
