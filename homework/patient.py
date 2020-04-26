import os.path
import os
import pandas as pd
import homework.logg as l

class Correct_name():

    def __get__(self, obj, type = None):
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        if value is not None:
            if obj._creat:
               obj.logger_error.error("You can't change the name that has been already written down")
               raise AttributeError()
            else:
                if isinstance(value, str):
                    if value.isalpha():
                      obj.__dict__[self.name] = value
                    else:
                        obj.logger_error.error('Name should have only the latter')
                        raise ValueError()
                else:
                    obj.logger_error.error('Name should have only the latter')
                    raise TypeError()

    def __set_name__(self, owner, name):
        self.name = name

class Patient():

    first_name = Correct_name()
    last_name = Correct_name()

    def __init__(self, f_name=None, l_name=None, b_date=None, phone_from=None, d_type=None, d_id=None):
      self.logger_new_change = l.logger_new_change
      self.logger_error = l.logger_error
      self._creat = False
      self.first_name = f_name
      self.last_name = l_name
      self.birth_date = b_date
      self.phone = phone_from
      self.document_type = d_type
      self.document_id = d_id
      if f_name != None:
          self.logger_new_change.info(['New patient', self.first_name])
      self._creat = True

    def __str__(self):
        return "f_name: {} \t l_name: {} \t b_date: {} \t phone: {} \t d_type: {} \t d_id: {}".format(self.first_name,
        self.last_name,  self.birth_date, self.phone,  self.document_type, self.document_id)

    def __del__(self):
        l.Error_handler.close()
        l.New_ChangePat_handler.close()


    @staticmethod
    def create(*args):
        return Patient(*args)

    def save(self):
        column = ['first name', 'last name', 'birthday date', 'phone number', 'document type', 'document id']
        data_to_save = {'first name': [self.first_name],
            'last name': [self.last_name], 'birthday date': [self.birth_date], 'phone number': [self.phone],
                        'document type': [self.document_type], 'document id': [self.document_id]}
        df = pd.DataFrame(data_to_save, columns = column)
        df.to_csv('Patients.csv', mode = 'a',encoding = "utf-8", index = False, header= False)

# Условие на тип документа

    @property
    def document_type(self):
        return self.d_type

    @document_type.setter
    def document_type(self, value):
        if value is not None and isinstance(value, str):
            if all(x.isalpha() or x == ' ' for x in value):
                value.strip()
                buf = False
                if value == 'паспорт' or value == 'Паспорт':
                    value = 'Паспорт'
                    buf = True
                elif value == 'заграничный паспорт' or value == 'Заграничный паспорт':
                    value = 'Заграничный паспорт'
                    buf = True
                elif value == 'водительское удостоверение' or value == 'права' or value == 'Права' \
                        or value == 'Водительское удостоверение':
                    value = 'Водительское удостоверение'
                    buf = True
                if buf == True:
                    if self._creat == True:
                        self.logger_new_change.info(["Document type is changed, the new one is ", value])
                    self.d_type = value
                else:
                    self.logger_error.error('You should write down only your passport')
                    raise ValueError()
            else:
                self.logger_error.error("Your doc type is incorrect")
                raise TypeError()
        else:
            self.logger_error.error("You didn't write down your document type")
            raise TypeError()

# Условие на номер телфона

    @property
    def phone(self):
        return self.phone_from

    @phone.setter
    def phone(self, value):
      if value is not None and isinstance(value, str):
        if all(x.isdigit() or x == ')' or x == '(' or x == '+' or x == '-' or x == ' ' for x in value):
            buf = []
            for x in value:
                if x.isdigit():
                    buf.append(x)
            if len(buf) == 11 and (int(buf[0]) == 8 or int(buf[0]) == 7) and int(buf[1]) == 9:
               buf.insert(0, '+')
               buf[1] = '7'
               buf.insert(2, '(')
               buf.insert(6, ')')
               buf.insert(10, '-')
               buf.insert(13, '-')
               final_str = ''
               value = final_str.join(buf)
               if self._creat == True:
                   self.logger_new_change.info(["Phone number is changed, the new one is ", value])
               self.phone_from = value
            else:
                self.logger_error.error(["The number is too long", value])
                raise ValueError()
        else:
            self.logger_error.error(["It's incorrect number type. Please, try again", value])
            raise ValueError()
      else:
          self.logger_error.error("You didn't write down your number phone")
          raise TypeError()


# Условие на документ
    @property
    def document_id(self):
        return self.d_id

    @document_id.setter
    def document_id(self, value):
      if value is not None and isinstance(value, str):
        flag = False
        if all(x.isdigit() or x == ' ' or x =='/' or x == '-' for x in value):
            buf = []
            for x in value:
                if x.isdigit():
                    buf.append(x)
            if self.document_type == "Паспорт" and len(buf) == 10:
                    flag = True
                    buf.insert(4, ' ')
                    final_str = ''
                    value = final_str.join(buf)
            elif self.document_type == "Заграничный паспорт" and len(buf) == 9:
                flag = True
                buf.insert(2, ' ')
                final_str = ''
                value = final_str.join(buf)
            elif self.document_type == "Водительское удостоверение" and len(buf) == 10:
                flag = True
                buf.insert(2, ' ')
                buf.insert(5, ' ')
                final_str = ''
                value = final_str.join(buf)
            else:
                self.logger_error.error("Incorrect passport_id")
                raise ValueError()
            if flag == True:
                if self._creat == True:
                    self.logger_new_change.info(["Document id is changed, the new one is ", value])
                self.d_id = value
        else:
            self.logger_error.error("Incorrect passport_id")
            raise ValueError()
      else:
          self.logger_error.error("You didn't write down your document id")
          raise TypeError()

# Условие на дату рождения

    @property
    def birth_date(self):
        return self.b_date

    @birth_date.setter
    def birth_date(self, value):
        if value is not None and isinstance(value, str):
            if all(x.isalnum() or x == '.' or x == ' ' or x == '-' for x in value): # Состоит ли строка только из цифр/ букв и . -
            # Определяю 3 ли входных данных
                if len(value.split('.')) == 3:
                    buf = value.split('.')
                elif len(value.split('-')) == 3:
                    buf = value.split('-')
                else:
                    buf = value.split()
                # Проверка на корректность входных данных
                if len(buf) == 3:
                    if not buf[0].isdigit() and not buf[2].isdigit():
                        self.logger_error.error(["Incorrect birth date", value])
                        raise ValueError()
                    month = ['Janury', 'Febrary', 'March', 'April', 'May', 'June', 'July', 'August', "September",
                             'October','November', 'December']
                    if 1 <= int(buf[0]) <= 31 and (buf[1].isdigit() or buf[1] in month) and 1800 <= int(buf[2]) <= 2020:
                        if buf[1].isdigit():
                            if 1 >= int(buf[1]) >= 12:
                                self.logger_error.error(["Incorrect birth date, month couldn't be more than 12", value])
                                raise ValueError()
                            buf.reverse()
                        final_str = '-'
                        value = final_str.join(buf)
                        if self._creat == True:
                            self.logger_new_change.info(["Birth date is changed, the new one is ", value])
                        self.b_date = value
                    elif 1800 <= int(buf[0]) <= 2020 and (buf[1].isdigit() or buf[1] in month) \
                            and 1 <= int(buf[2]) <= 31:
                        if buf[1].isdigit():
                            if 1 >= int(buf[1]) >= 12:
                                self.logger_error.error(["Incorrect birth date, month couldn't be more than 12", value])
                                raise ValueError()
                        final_str = '-'
                        value = final_str.join(buf)
                        if self._creat == True:
                            self.logger_new_change.info(["Birth date is changed, the new one is ", value])
                        self.b_date = value
                    else:
                        self.logger_error.error("Yoy birth date is incorrect")
                        raise ValueError()
                else:
                    self.logger_error.error("Yoy birth date is incorrect")
                    raise ValueError()
            else:
                self.logger_error.error("Yoy birth date is incorrect")
                raise ValueError()
        else:
            self.logger_error.error("You didn't write down your birthday")
            raise TypeError()

class PatientCollection():
    def __init__(self, path_to_file):
        self._path_to_file = path_to_file
        if os.path.exists(self._path_to_file) == False:
            raise ValueError()

    def __iter__(self):
        with open(self._path_to_file, 'r', encoding='utf-8') as filehandle:
            for line in filehandle:
                line = line.replace('\n', '')
                line = line.split(',')
                yield Patient(*line)

    def limit(self, range):
        with open(self._path_to_file, 'r', encoding='utf-8') as filehandle:
            count = 1
            for line in filehandle:
                line = line.replace('\n', '')
                line = line.split(',')
                if count <= range:
                    yield Patient(*line)
                count += 1

