from pprint import pprint
import re
import numpy as np

# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
# 1
def FIO_note(row_num):
  row = contacts_list[row_num]
  #print(row)

  # Ф+ИО:
  if row[1]!='' and row[2]=='':
    text_IO = row[1]
    words = text_IO.split(' ')
    if len(words)==1:
      row[1] = words[0]    #если нет отчества
    else:
      row[1], row[2] = words[0], words[1] # если есть отчество
    #print(row)

  # ФИ +О:
  if row[1]=='' and row[2]!='':
    text_FI= row[0]
    words = text_FI.split(' ')
    row[0], row[1] = words[0], words[1]
    #print(row)

  # ФИО:
  if row[1]=='' and row[2]=='':
    text_FIO= row[0]
    words = text_FIO.split(' ')

    if len(words)==3:
      row[0], row[1], row[2] = words[0], words[1], words[2] #если есть отчество
    else:
      row[0], row[1] = words[0], words[1]  #если нет отчества

  contacts_list[row_num] = row

# 2
def phone_converter(row_num):
  row = contacts_list[row_num]
  phone = row[5]
  #print(phone)

  if phone == '':
    contacts_list[row_num][5] = ''
    return ''
  else:
    results= re.split(r'доб\.', phone, flags=re.IGNORECASE)

  extension = None
  if len(results)==1:
    phone_number = results[0]
  else:
    phone_number, extension = results[0], results[1]
    extension = re.sub(r'\D', '', extension)

  phone_number = re.sub(r'\D', '', phone_number)

  if len(phone_number)!=11:
    contacts_list[row_num][5] ="Некорректный номер телефона"
    return "Некорректный номер телефона"

  if extension==None:
    contacts_list[row_num][5] = f"+7({phone_number[1:4]}){phone_number[4:7]}-{phone_number[7:9]}-{phone_number[9:11]}"
  else:
    contacts_list[row_num][5] = f"+7({phone_number[1:4]}){phone_number[4:7]}-{phone_number[7:9]}-{phone_number[9:11]} доб.{extension}"



# 3
def remove_duplicates(input_list):
  seen = set()
  unique_list = []

  for item in input_list:
    # Преобразуем подсписок в строку, чтобы использовать регулярные выражения
    item_str = ','.join(map(str, item))

    match = re.match(r'([^,]+,[^,]+)', item_str)

    if match:
      key = match.group(1)  # Получаем первые два элемента как ключ

      if key not in seen:
        seen.add(key)
        unique_list.append(item)

  return unique_list

for row in range(1,len(contacts_list)):
  FIO_note(row)
  phone_converter(row)

contacts_list = remove_duplicates(contacts_list)
print(contacts_list)


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)