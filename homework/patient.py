import logg as l
from mysql.connector import MySQLConnection
from mySQL_config import read_db_config

db_config = read_db_config()
mydb = MySQLConnection(**db_config)
mycursor = mydb.cursor()
sqlFormula = "INSERT INTO patients (first_name, last_name, datebirth," \
             " phone_number, passport_type, passport_id) VALUES (%s, %s, %s, %s, %s, %s)"

def my_log_info(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            if  self._text_to_logg!= None:
                self.logger_new_change.info(self._text_to_logg)
                self._text_to_logg = None
        return wrapper

def my_logging_decorator(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except ValueError:
            self.logger_error.error('ValueError')
            raise
        except TypeError:
            self.logger_error.error('TypeError')
            raise
        finally:
            if self._text_to_logg != None:
                self.logger_new_change.info(self._text_to_logg)
                self._text_to_logg = None
    return wrapper


class Correctname():

    def __get__(self, obj, type = None):
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        if value is not None:
            if obj._creat:
               raise AttributeError()
            else:
                if isinstance(value, str):
                    if value.isalpha():
                      obj.__dict__[self.name] = value
                    else:
                        raise ValueError()
                else:
                    raise TypeError()

    def __set_name__(self, owner, name):
        self.name = name

class Patient():

    first_name = Correctname()
    last_name = Correctname()
    _text_to_logg = None

    def __init__(self, _f_name=None, _l_name=None, _b_date=None, _phone_from=None, _d_type=None, _d_id=None):
      self.logger_new_change = l.logger_new_change
      self.logger_error = l.logger_error
      self._creat = False
      self.first_name = _f_name
      self.last_name = _l_name
      self.birth_date = _b_date
      self.phone = _phone_from
      self.document_type = _d_type
      self.document_id = _d_id
      if _f_name != None:
          self._text_to_logg = 'New Patient'
      self._creat = True

    def __str__(self):
        return "f_name: {} \t l_name: {} \t b_date: {} \t phone: {} \t d_type: {} \t d_id: {}".format(self.first_name,
        self.last_name,  self.birth_date, self.phone,  self.document_type, self.document_id)

    def __del__(self):
        l.error_handler.close()
        l.new_ChangePat_handler.close()


    @staticmethod
    def create(*args):
        return Patient(*args)

    def save(self):
        date2 = (self.first_name, self.last_name, self.birth_date, self.phone, self.document_type,
                self.document_id)
        mycursor.execute(sqlFormula, date2)
        mydb.commit()

# Условие на тип документа

    @property
    def document_type(self):
        return self._d_type

    @document_type.setter
    @my_log_info
    def document_type(self, value):
        if isinstance(value, str):
            value.strip()
            versions = ['Паспорт', 'паспорт', 'заграничный паспорт', 'Заграничный паспорт', 'Водительское удостоверение', 'водительское удостоверение']
            if value in versions:
                for x in versions:
                    if value == x:
                        value = x.capitalize()
                        break
                if self._creat == True:
                    self._text_to_logg = 'Document type is changed'
                self._d_type = value
            else:
                raise ValueError()

        else:
            raise TypeError()

# Условие на номер телфона

    @property
    def phone(self):
        return self._phone_from

    @phone.setter
    @my_log_info
    def phone(self, value):
      if value is not None and isinstance(value, str):
        if all(x.isdigit() or (x in "()+- ") for x in value):
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
                   self._text_to_logg = 'Phone number is changed'
               self._phone_from = value
            else:
                raise ValueError()
        else:
            raise ValueError()
      else:
          raise TypeError()


# Условие на документ
    @property
    def document_id(self):
        return self._d_id

    @document_id.setter
    @my_log_info
    def document_id(self, value):
      if value is not None and isinstance(value, str):
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
                    self._text_to_logg = 'Phone id is changed'
                self._d_id = value
        else:
            raise ValueError()
      else:
          raise TypeError()

# Условие на дату рождения

    @property
    def birth_date(self):
        return self._b_date

    @birth_date.setter
    @my_log_info
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
                        raise ValueError()
                    month = ['Janury', 'Febrary', 'March', 'April', 'May', 'June', 'July', 'August', "September",
                             'October','November', 'December']
                    if 1 <= int(buf[0]) <= 31 and (buf[1].isdigit() or buf[1] in month) and 1800 <= int(buf[2]) <= 2020:
                        if buf[1].isdigit():
                            if 1 >= int(buf[1]) >= 12:
                                raise ValueError()
                            buf.reverse()
                        final_str = '-'
                        value = final_str.join(buf)
                        if self._creat == True:
                            self._text_to_logg = 'Birth date is changed'
                        self._b_date = value
                    elif 1800 <= int(buf[0]) <= 2020 and (buf[1].isdigit() or buf[1] in month) \
                            and 1 <= int(buf[2]) <= 31:
                        if buf[1].isdigit():
                            if 1 >= int(buf[1]) >= 12:
                                raise ValueError()
                        final_str = '-'
                        value = final_str.join(buf)
                        if self._creat == True:
                            self._text_to_logg = 'Birth date is changed'
                        self._b_date = value
                    else:
                        raise ValueError()
                else:
                    raise ValueError()
            else:
                raise ValueError()
        else:
            raise TypeError()

class PatientCollection():

    def __init__(self):
        pass

    def __iter__(self):
        mycursor.execute("SELECT * FROM patients")
        pats = mycursor.fetchone()
        if pats == None:
            return 0
        while pats is not None:
            yield Patient(*pats)
            pats = mycursor.fetchone()

    def limit(self, range):
        mycursor.execute("SELECT * FROM patients")
        count = 0
        while count is not range:
            pats = self._mycursor.fetchone()
            if pats is not None:
                yield Patient(*pats)
                count += 1
            else:
                if count == 0:
                    print("В БД нет ни одного пациента")
                    return 0
                else:
                    print("Пациентов меньше чем ", range)
                break

mycursor.close()
mydb.close()