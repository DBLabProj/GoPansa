import pymysql
import time

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
    

    # 수정 -------------------------------------------- 
    # 회원가입하는 함수
    # input: id, password, name, phone_number, email
    # output: 1(완료), 2(ID 중복), 3(PW규칙위반), 4(SQL모듈에러)
    def register(self, id, pw, name, phone=None, email=None):
        if len(pw) < 6:
            return 3 #PW 규칙위반
        sql = "INSERT INTO user VALUES(%s, %s, %s, %s, %s, %s, %s, %s);";

        try:
            self.__cursor.execute(sql, (id, pw, "dummy", "N", name, None, phone, email))
            self.__db.commit()
        except pymysql.err.IntegrityError as e:
            print(e)
            return 2 #ID 중복
        except pymysql.Error as e:
            print(e)
            return 4
        
        return 1

    # 수정 -------------------------------------------- 
    def regi_store(self, name, user_id, latitude, longitude, address=None, tel=None, time=None):
        sql = "INSERT INTO store VALUES(%s, %s, %s, %s, %s, %s, %s);"

        try:
            self.__cursor.execute(sql, (name, user_id, latitude, longitude, address, tel, time))
            self.__db.commit()
        except pymysql.Error as e:
            print(e)
            return 2
        return 1

    # user의 등급을 바꾸는 함수
    # input: user_id(아이디), grade(바꿀 등급)
    # output: 1(정상), 2(SQL에러), 3(grade 형식 오류)
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

    # user의 등급을 받는 함수
    # input: user_id(아이디)
    # output: grade(정상), 2(SQL에러), 3(유저 없음)
    def get_user_grade(self, user_id):
        sql = "SELECT grade FROM user WHERE id=%s"
        #   N  B P
        try:
            self.__cursor.execute(sql, user_id)
            result = self.__cursor.fetchone()
        except pymysql.Error as e:
            print(e)
            return 2 #sql에러

        if result is None:
            return 3 #ID없음
        
        return result['grade']


    # 해당유저 등급이 None인지 구별하는 함수
    # input: user_id
    # output: boolean(정상), 2(SQL에러), 3(ID없음)
    def is_user_none(self, user_id):
        grade = self.get_user_grade(user_id)

        if grade == "N":
            return True
        elif type(grade) == str:
            return False
        else:
            return grade


    # 해당유저 등급이 None인지 구별하는 함수
    # input: user_id
    # output: boolean(정상), 2(SQL에러), 3(ID없음)
    def is_user_basic(self, user_id):
        grade = self.get_user_grade(user_id)

        if grade == "B":
            return True
        elif type(grade) == str:
            return False
        else:
            return grade


    # 해당유저 등급이 None인지 구별하는 함수
    # input: user_id
    # output: boolean(정상), 2(SQL에러), 3(ID없음)
    def is_user_premium(self, user_id):
        grade = self.get_user_grade(user_id)

        if grade == "N":
            return True
        elif type(grade) == str:
            return False
        else:
            return grade



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


    # DB에서 원하는 데이터를 가져오는 함수
    # 첫째인자 : 가져올 칼럼
    # 둘째인자 : 테이블명
    # 셋째인자 : 뒷부분에 가져올 조건 (where 등)
    # 반환값 : 해당 조건으로 검색된 데이터
    def get_data_from_db(self, selection, table, target):
        with self.__cursor as cursor:
            result = 0

            sql_qur = f'select {selection} from {table} {target}'
            
            cursor.execute(sql_qur)
            result = cursor.fetchall()
            
            if result == ((None,),):
                result = [["-1"]]
            
            return result




    def get_store(self):
        sql = "SELECT * FROM store"

        try:
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
        except pymysql.Error as e:
            print(e) 
        
        return result
        
        
    def getStoreList(self, storeName):
        sql = "\
            SELECT cb_number, business_name \
            FROM restaurant \
            WHERE business_name LIKE '%"+storeName+"%';\
            "
        # print(sql)
        storeList = []
        try:
            self.__cursor.execute(sql)
            storeList = self.__cursor.fetchall()
            # storeList = [x for x in self.__cursor.fetchall()]
            
            # print("storeList>>",len(storeList))
            # return storeList
        except pymysql.Error as e:
            print(e)
            return ["현재 서비스에 장애가 발생하였습니다."]
            
        return storeList
            
        
    def getStoreAddr(self, store_id):
        sql = "\
            SELECT address \
            FROM restaurant \
            WHERE cb_number ="+store_id+";\
            "
        try:
            self.__cursor.execute(sql)
            store_addr = self.__cursor.fetchone()
            print(store_addr)
        except pymysql.Error as e:
            print(e)
            return "현재 서비스에 장애가 발생하였습니다."
            
        return store_addr
    

    # 오늘날짜 불러오는 함수
    # input: none
    # output: str(yymmdd)
    def __get_today(self):
        return time.strftime("%y%m%d", time.localtime(time.time()))
    
    # 현재시간 불러오는 함수
    # input: none
    # output: str(yymmdd)
    def __get_datetime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))


    # 측정 일련번호 생성을 위해 해당 날짜에서 측정이 몇번 이뤄줬는지 확인하는 함수
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


# sql = Sql('203.252.240.74', 'classify_meat', 'dblab', 'dblab6100')
# print(sql.register('admin', 'dblab6100', '양희범'))
# sql.regi_store('도깨비축산물', 'admin', 36.6533668, 127.4795429, '충북 청주시 청원구 교서로196번길 19 도깨비축산물', '043-224-5195', '매일 09:00 - 20:30')
# sql.regi_store('다성축산유통', 'admin', 36.6340571, 127.5043006, '충북 청주시 상당구 교동로 163 1층', '043-292-3864', '매일 09:00 - 21:00 연중무휴')
# sql.regi_store('괴산불고기정육점', 'admin', 36.6289958, 127.4781339, '충북 청주시 서원구 모충로 137', '043-256-7144', '매일 09:00 - 21:00 연중무휴')
# sql.regi_store('주성고기', 'admin', 36.6224571, 127.4420045, '충북 청주시 흥덕구 가경로 72', '043-237-6689', '매일 09:00 - 21:00')
# sql.regi_store('일진정육백화점', 'admin', 36.6701363, 127.4897753, '충북 청주시 청원구 율봉로185번길 17', '043-217-5747', '매일 09:00 ~ 20:30')
# sql.regi_store('가덕암소한우정육점', 'admin', 36.6232368, 127.4280521, '충북 청주시 흥덕구 서현중로 53-1', '043-231-7293', '매일 08:30 ~ 21:00')
# sql.regi_store('두릅소축산물백화점 율량점', 'admin', 36.6715480, 127.4992033, '충북 청주시 청원구 율량로 122', '043-292-3700', '매일 09:00 ~ 21:00')
# sql.regi_store('정육시대', 'admin', 36.6113230, 127.4656896, '충북 청주시 서원구 산남로 76', '043-288-0667', '매일 09:00 - 21:00 연중무휴')
# sql.regi_store('센트럴축산', 'admin', 36.7129423, 127.4224550, '충북 청주시 청원구 오창읍 오창공원로 96 상가동 117호', '010-4004-1411', '매일 09:00 - 21:00')
# sql.regi_store('삼성축산', 'admin', 36.7094003, 127.4298425, '충북 청주시 청원구 오창읍 과학산업3로 227 우림필유1차아파트 상가동 101호', '043-211-0072', '매일 08:00 - 22:00')
# sql.regi_store('오창축산물', 'admin', 36.7386415, 127.4506360, '충북 청주시 청원구 오창읍 2산단4로 55 108동 오창축산물', '043-214-1253', '매일 09:00 - 21:00 연중무휴')

# result = sql.get_store()
# for row in result:
#     print(row)