import numpy as np
import string
import datetime
import pandas as pd
from faker import Faker

icd_file = pd.ExcelFile("ICD-10.xlsx")
icd_cm_dataframe = pd.read_excel(icd_file, '2021中文版_cm')
icd_pcs_dataframe = pd.read_excel(icd_file, '2021中文版_pcs')
departments = '家庭醫學科、內科、外科、兒科、婦產科、骨科、神經科、神經外科、泌尿科、耳鼻喉科、眼科、皮膚科、精神科、復健科、麻醉科、放射診斷科、放射腫瘤科、解剖病理科、臨床病理科、核子醫學科、急診醫學科、整形外科、職業醫學科、西醫一般科、牙醫一般科、口腔病理科、口腔顎面外科、齒顎矯正科、牙周病科、兒童牙科、牙髓病科、牙體復形科、家庭牙醫科、中醫一般科、中醫內科、中醫外科、中醫眼科、中醫兒科、中醫婦科、中醫傷科、中醫針灸科、中醫痔科'.split('、')

def create_content(disease_amount: int, doc_length=10) -> dict:
    result = {
        'gender': get_random_gender(),
        'name': get_random_name(),
        'doc_num': get_random_doc_num(doc_length),
        'address': get_random_address(),
        'roc_date': get_random_roc_date(),
        'id_card': get_random_id_card_num(),
        'disease': get_muiltiple_disease_name(disease_amount),
        'advise': get_random_advise(),
        'roc_year': str(np.random.randint(30, 100)),
        'month': str(np.random.randint(1, 13)),
        'day': str(np.random.randint(1, 29)),
        'dept': get_random_dept()
    }
    return result

def get_random_dept() -> str:
    random_num = np.random.randint(len(departments))
    return departments[random_num]

def get_random_gender() -> str:
    if flip_coin():
        return '女'
    else:
        return '男'

def get_random_doc_num(lenth = 10) -> str:
    return str(np.random.randint(10*(lenth+1)-1)).zfill(lenth)

def get_random_name() -> str:
    faker = Faker('zh_TW')
    return faker.name()

def get_random_address() -> str:
    faker = Faker('zh_TW')
    return faker.address()

def get_random_year() -> str:
    return str(np.random.randint(30,100))

def get_random_month() -> str:
    return str(np.random.randint(1,13))

def get_random_day() -> str:
    return str(np.random.randint(1,29))

def get_random_roc_date() -> str:
    today = datetime.date.today()
    random_day = np.random.randint(10, 30000)
    generated_day = today - datetime.timedelta(random_day)
    formated_day = str(generated_day.year-1911) + '/' + str(generated_day.month) + '/' + str(generated_day.day)
    return formated_day

def get_random_id_card_num() -> str:
    random_place = string.ascii_uppercase[np.random.randint(0, 26)]
    random_gender = str((np.random.randint(1,10)%2) + 1)
    random_code = str(np.random.randint(0,99999999)).zfill(8)
    id_card_num = random_place + random_gender + random_code
    return id_card_num

def get_muiltiple_disease_name(amount: int) -> str:
    diseases = []
    for i in range(amount):
        diseases.append(get_random_disease_name())
    return ', '.join(diseases)

def get_random_disease_name() -> str:
    random_num = np.random.randint(0, icd_cm_dataframe.shape[0])
    disease = icd_cm_dataframe['中文名稱'][random_num]
    return disease

def get_random_advise() -> str:
    result = ''
    if flip_coin():
        result += '病人因上述原因，'
    if flip_coin():
        result += get_clinic()
    elif flip_coin():
        result += '於民國'
        result += get_random_roc_date()
        result += '來本院急診，'
    if flip_coin():
        result += '於民國'
        result += get_random_roc_date()
        result += '住院，'
    elif flip_coin():
        result += '於民國'
        result += get_random_roc_date()
        result += '進入加護病房觀察，'
        result += '民國'
        result += get_random_roc_date()
        result += '轉普通病房住院，'
    if flip_coin():
        result += get_operation_description()
    if flip_coin():
        result += '宜於門診持續追蹤治療'
    elif flip_coin():
        result += '不宜進行激烈運動'
    else:
        result += '宜多休息'
    result += '--以下空白--'
    return result

def get_clinic() -> str:
    clinic_count = np.random.randint(1,10)
    result = '於' + get_random_roc_date()
    for i in range(1, clinic_count):
        result += '、' + get_random_roc_date()
    result += '至門診就診，'
    return result

def get_operation_description() -> str:
    result = '於民國'
    result += get_random_roc_date()
    result += '接受'
    result += get_random_operation()
    result += '手術'
    return result

def get_random_operation() -> str:
    random_num = np.random.randint(0, icd_pcs_dataframe.shape[0])
    operation = icd_pcs_dataframe['中文名稱'][random_num]
    return operation

def flip_coin() -> bool:
    coin_face = np.random.randint(1, 10) % 2
    if coin_face == 1:
        return True
    else:
        return False