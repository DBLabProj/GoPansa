import pymysql

class Sql:
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
        

    # get data that is filtered by id from database
    # input: 'no' in classify_meat record you want to find
    # output: result(dictionary)
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
    
    
    # 아이디가 존재하는지 확인하는 함수
    # input: id
    # output: True(존재), False(없음)
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
    

    # 회원가입하는 함수
    # input: id, password, name, phone_number, email
    # output: 1(완료), 2(ID 중복), 3(PW규칙위반), 4(SQL모듈에러)
    def register(self, id, pw, name, phone=None, email=None):
        if len(pw) < 6:
            return 3 #PW 규칙위반
        sql = "INSERT INTO user VALUES(%s, %s, %s, %s, %s, %s);";

        try:
            self.__cursor.execute(sql, (id, pw, "dummy", name, phone, email))
            self.__db.commit()
        except pymysql.err.IntegrityError as e:
            print(e)
            return 2 #ID 중복
        except pymysql.Error as e:
            print(e)
            return 4
        
        return 1


    # 로그인 함수
    # input: id, password
    # output: 1(완료), 2(ID 없음), 3(PW틀림), 4(SQL모듈에러)
    def login(self, id, pw):
        sql = "\
        SELECT pw FROM user WHERE id=%s;"
        try:
            self.__cursor.execute(sql, id)
            result = self.__cursor.fetchone()
        except pymysql.Error as e:
            print(e)
            return 4 #sql에러

        if result is None:
            return 2 #ID없음
        else:
            if result['pw'] == pw:
                return 1 #완료
            else:
                return 3 #PW틀림


    def regi_store(self, name, user_id, latitude, longitude, address=None, tel=None, time=None):
        sql = "INSERT INTO store VALUES(%s, %s, %s, %s, %s, %s, %s);"

        try:
            self.__cursor.execute(sql, (name, user_id, latitude, longitude, address, tel, time))
            self.__db.commit()
        except pymysql.Error as e:
            print(e)
            return 2
        return 1


    def get_store(self):
        sql = "SELECT * FROM store"

        try:
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
        except pymysql.Error as e:
            print(e) 
        
        return result
