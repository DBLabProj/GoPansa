import pymysql
import time

class Sql:
    # constructor > connect to external mysql server
    # input: host(server IP), db(database name), user(id), password
    # output: None(if connecting is failed, this function'll call exception.)
    def __init__(self, host, db, user, password):
        try:
            self.__db = pymysql.connect(
                user=user, 
                passwd=password, 
                host=host,
                db=db, 
                charset='utf8')
            self.__cursor = cursor = self.__db.cursor(pymysql.cursors.DictCursor)
        except pymysql.Error as e:
            code, msg = e.args
            print(code, msg)



    # register user account with value inputed
    # input: id, password, name, phone_number, email
    # output: 1(OK), 2(ID Duplication), 3(violation of PW rules), 4(SQL Module error)
    def register(self, id, pw, name, main_store, phone=None, email=None):
        if len(pw) < 6:
            return 3 #violation of PW rules
        sql = "INSERT INTO user VALUES(%s, %s, %s, %s, %s, %s, %s, %s);";

        try:
            self.__cursor.execute(sql, (id, pw, "dummy", "N", name, main_store, phone, email))
            self.__db.commit()
        except pymysql.err.IntegrityError as e:
            print(e)
            return 2 #ID 중복
        except pymysql.Error as e:
            print(e)
            return 4
            
        return 1


    # login
    # input: id, password
    # output: 1(OK), 2(ID is not exist), 3(PW incorrect), 4(SQL Modlue error)
    def login(self, id, pw):
        sql = "SELECT pw FROM user WHERE id=%s;"
        try:
            self.__cursor.execute(sql, id)
            result = self.__cursor.fetchone()
        except pymysql.Error as e:
            print(e)
            return 4 #SQL Modlue error

        if result is None:
            return 2 #ID is not exist
        else:
            if result['pw'] == pw:
                return 1 #OK
            else:
                return 3 #PW incorrect

    
    # check the id is exist
    # input: id
    # output: True(if it's exist), False(if it's not exist)
    # if there's sql error, the function'll call the exception with code and error message.
    def is_id_exist(self, id):
        try:
            sql = "\
            SELECT  1\
            FROM    user\
            WHERE   id = + '" + id + "';"

            self.__cursor.execute(sql)
            result = self.__cursor.fetchone()
        except pymysql.Error as e:
            code, msg = e.args
            print(code, msg)

        if result is None:
            return False
        else:
            return True



    # change the user grade
    # input: user_id, grade(grade value you want to change)
    # output: 1(OK), 2(SQL moudule rror), 3(violation of grade value rules)
    def set_user_grade(self, user_id, grade):
        if grade not in("N", "B", "P"):
            return 3
        sql = "UPDATE user SET grade=%s WHERE id=%s"
        try:
            self.__cursor.execute(sql, (grade, user_id))
            self.__db.commit()
        except pymysql.Error as e:
            print(e)
            return 2
        return 1


    # get user grade from connected db
    # input: user_id(user id you want to find grade)
    # output: grade(string, OK), 2(SQL module error), 3(user is not exist in db)
    def get_user_grade(self, user_id):
        sql = "SELECT grade FROM user WHERE id=%s"
        try:
            self.__cursor.execute(sql, user_id)
            result = self.__cursor.fetchone()
        except pymysql.Error as e:
            print(e)
            return 2 #SQL Modlue error

        if result is None:
            return 3 #ID is not exist
        
        return result['grade']


    # store classification result to database
    # input: user_id, image_name,  meat_type, grade
    # output: classification serial number(OK), error message(SQL ERROR)
    def insert_classify_data(self, user_id, image_name, meat_type, grade):
        sql = "INSERT INTO classify VALUES(%s, %s, %s, %s, %s, %s);"
        count = self.__classify_count()
        today = self.__get_today()
        no = today + "-" + meat_type + count
        datetime = self.__get_datetime()

        try:
            self.__cursor.execute(sql, (no, datetime, user_id, image_name, meat_type, grade))
            self.__db.commit()
        except pymysql.Error as e:
            print(e)
            
        return no


    # bring the classify record from connected db
    # input: 'no' in classify_meat record you want to find
    # output: record(dictionary), -1(if it's not exist)
    def get_classify_result_data(self, no):
        sql ="\
            SELECT   c.no, c.datetime, c.meat_type, c.grade, c.image_name, u.main_store, r.address\
            FROM     classify c, user u, restaurant r\
            WHERE    c.user_id = u.id\
            AND      u.main_store = r.business_name\
            AND      c.no = %s"
        
        try:
            self.__cursor.execute(sql, no)
            result = self.__cursor.fetchone()
        except pymysql.Error as e:
            print(e)
        
        if result is None:
            return -1
        else:
            if result['meat_type'] == "P":
                result['meat_type'] = "돼지고기"
            elif result['meat_type'] == "B":
                result['meat_type'] = "소고기"
            else:
                return -1

            result['datetime'] = str(result['datetime'])

        return result


    # determine how many classification have been made today to generate serial numbers
    # input: none
    # output: str(Ex. 0005)
    def __classify_count(self):
        today = self.__get_today()

        sql = "\
            SELECT  count(date_format(datetime, '%y%m%d')) num\
            FROM    classify\
            WHERE   date_format(datetime, '%y%m%d')=" + today + ";"

        try:
            self.__cursor.execute(sql)
            result = self.__cursor.fetchone()
        except pymysql.Error as e:
            print(e)
        
        if result is None:
            num = 1 # 결과없으면 1부터 시작
        else:
            num = result['num'] + 1 #결과있으면 개수+1임
        
        return str(num).zfill(4) # 0004 문자열 형식으로 출력



    # get data that is filtered by id from database
    # input: 'no' in classify_meat record you want to find
    # output: result(dictionary), -1(No search results)
    def get_labeldata(self, no):
        try:
            cursor = self.__db.cursor(pymysql.cursors.DictCursor)

            sql = "\
            SELECT  c.no, c.datetime, u.name, c.meat_type, c.grade\
            FROM    user u, classify c\
            WHERE   no = '" + no + "'"

            cursor.execute(sql)
            result = cursor.fetchone()
        except pymysql.Error as e:
            code, msg = e.args
            print(code, msg)

        
        if result is None:
            print('검색결과가 없습니다.')
            return -1
        else:
            result['datetime'] = str(result['datetime'])
        
        return result
    
    
    # register store to database
    # input: name(business name), user_id, latitude, longitude << this parameters is necessary.
    #        address, tel(store telephone number), time(opening and closing time) <<  this parameters is optional.
    # output: 1(OK), 2(SQL module error)
    def regi_store(self, name, user_id, latitude, longitude, address=None, tel=None, time=None):
        sql = "INSERT INTO store VALUES(%s, %s, %s, %s, %s, %s, %s);"

        try:
            self.__cursor.execute(sql, (name, user_id, latitude, longitude, address, tel, time))
            self.__db.commit()
        except pymysql.Error as e:
            print(e)
            return 2
        return 1


    # get store list(it is registed by user directly)
    # input: none
    # output: result(dictionary)
    def get_store(self):
        sql = "SELECT * FROM store"

        try:
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
        except pymysql.Error as e:
            print(e) 
        
        return result
        
        

    # get store number, name with store name inputed.
    # input: store name
    # output: result(List)
    def getStoreList(self, storeName):
        sql = "\
            SELECT cb_number, business_name \
            FROM restaurant \
            WHERE business_name LIKE '%"+storeName+"%';\
            "
        storeList = []
        try:
            self.__cursor.execute(sql)
            storeList = self.__cursor.fetchall()
        except pymysql.Error as e:
            print(e)
            return ["현재 서비스에 장애가 발생하였습니다."]
            
        return storeList
            
    
    # get store address with store id inputed.
    # input: store id
    # output: result(dictionary)
    def getStoreAddr(self, store_id):
        sql = "\
            SELECT address \
            FROM restaurant \
            WHERE cb_number ="+store_id+";\
            "
        try:
            self.__cursor.execute(sql)
            store_addr = self.__cursor.fetchone()
        except pymysql.Error as e:
            print(e)
            return "현재 서비스에 장애가 발생하였습니다."
            
        return store_addr


    # get the data you want from conntect db
    # input: selection(column to import), table(db table name), target(additional statements(EX. where))
    # output: result(Data retrieved under these conditions)
    def get_data_from_db(self, selection, table, target):
        with self.__cursor as cursor:
            result = 0

            sql_qur = f'select {selection} from {table} {target}'
            
            try:
                cursor.execute(sql_qur)
                result = cursor.fetchall()

                if result == ((None,),):
                    result = [["-1"]]
            except pymysql.Error as e:
                print(e)
            
            
            return result


    # get today's date
    # input: none
    # output: str(yymmdd)
    @staticmethod
    def __get_today():
        return time.strftime("%y%m%d", time.localtime(time.time()))
    

    # get current datetime
    # input: none
    # output: str(yymmdd hh:mm:ss)
    @staticmethod
    def __get_datetime():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))