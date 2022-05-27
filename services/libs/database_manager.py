from enum import Enum
import pymysql
import re
import os

class TableName(Enum):
    LISTINGS = "listing"
    LISTING_PHOTOS = "listing_photos"
    CATEGORIES = "categories"
    
    def get(self,item):
        return item.value
    
    def get_name(self,item):
        return item.name

class ScraperName(Enum):
    URL_SCRAPER = "url_scraper"
    DEALER_SCRAPER = "dealer_scraper"
    def get(self,item):
        return item.value
    
    def get_name(self,item):
        return item.name

class ScraperType(Enum):
    NORMAL = "normal"
    VALIDATOR = "validator"

class Status(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    PENDING = "pending"
    SOLD = "sold"
    APPROVAL = "approval"
    MANUAL_EXPIRE = "manual_expire"
    TO_PARSE = "to_parse"
    def get(self,item):
        return item.value
    
    def get_name(self,item):
        return item.name

class Listings(Enum):
    ID = "id"
    SOURCE_ID = "source_id"
    SCRAPER_NAME = "scraper_name"
    CATEGORY_ID = "category_id"
    WEBSITE_ID = "website_id"
    VIDEO_ID = "video_id"
    DEALER_ID = "dealer_id"
    DEALER_NAME = "dealer_name"
    DEALER_LOCATION = "dealer_location"
    DEALER_NUMBER = "dealer_number"
    PRICE_INDICATOR = "price_indicator"
    PRIORITY = "priority"
    VEHICLE_TYPE = "vehicle_type"
    MAIN_PHOTO = "main_photo"
    PHOTOS_COUNT = "photos_count"
    STATUS = "status"
    WHY = "why"
    MM_PRICE = "mm_price"
    DISCOUNT = "discount"
    ADMIN_FEE = "admin_fees"
    MARGIN = "margin"
    CUSTOM_PRICE = "custom_price"
    CAP_CLEAN_PRICE = "cap_clean_price"
    CAL_PRICE_FROM_API = "cal_price_from_api"
    CAL_PRICE_FROM_FILE = "cal_price_from_file"
    PCP_MONTHLY_PRICE = "pcp_monthly_price"
    APR_MONTHLY_PRICE = "apr_monthly_price"
    MONTHLY_PRICE = "monthly_price"
    TITLE = "title"
    
    MAKE = "make"
    PREDICTED_MAKE = "predicted_make"
    
    MODEL = "model"
    PREDICTED_MODEL = "predicted_model"
    
    ENGINE_CYLINDER_CC = "engine_cylinder_cc"
    ENGINE_CYLINDER_LITRE = "engine_cylinder_litre"
    
    FUEL = "fuel"
    MILEAGE = "mileage"
    
    DOORS = "doors"
    
    SEATS = "seats"
    PREDICTED_SEATS = "predicted_seats"
    
    EMISSION_SCHEME = "emission_scheme"
    
    CREATED_TS = "created_ts"
    
    STOCK_TYPE = "stock_type"
    
    NUMBER_PLATE_FLAG = "number_plate_flag"
    
    QCF_OODLE_AB = "qcf_oodle_ab"
    QCF_OODLE_C = "qcf_oodle_c"
    QCF_BILLING = "qcf_billing"
    GCC = "gcc"
    AM_TIER_IN = "am_tier_in"
    AM_TIER_EX = "am_tier_ex"
    QCF_ADV_E = "qcf_adv_e"
    QCF_ADV_D = "qcf_adv_d"
    QCF_ADV_C = "qcf_adv_c"
    QCF_ADV_AB = "qcf_adv_ab"
    QCF_SMF = "qcf_smf"
    QCF_MB_NT = "qcf_mb_nt"
    QCF_MB_T = "qcf_mb_t"
    BMF = "bmf"
    O_O69 = "0-069"
    O_O79 = "0-079"
    O_O89 = "0-089"
    O_O99 = "0-099"
    O_109 = "0-109"
    O_119 = "0-119"
    O_129 = "0-129"
    O_139 = "0-139"
    O_149 = "0-149"
    O_159 = "0-159"
    O_169 = "0-169"
    O_179 = "0-179"
    O_189 = "0-189"
    O_199 = "0-199"
    O_209 = "0-209"
    O_219 = "0-219"
    O_229 = "0-229"
    O_239 = "0-239"
    O_249 = "0-249"
    O_259 = "0-259"
    O_269 = "0-269"
    O_279 = "0-279"
    O_289 = "0-289"
    O_299 = "0-299"
    O_309 = "0-309"
    O_319 = "0-319"
    O_329 = "0-329"
    O_339 = "0-339"
    O_349 = "0-349"
    O_359 = "0-359"
    O_369 = "0-369"
    O_379 = "0-379"
    O_389 = "0-389"
    O_399 = "0-399"
    O_409 = "0-409"
    O_419 = "0-419"
    O_429 = "0-429"
    O_439 = "0-439"
    O_449 = "0-449"
    O_459 = "0-459"
    O_469 = "0-469"
    O_479 = "0-479"
    O_489 = "0-489"
    O_499 = "0-499"
    O_299_48 = "0-299_48"
    O_399_48 = "0-399_48"
    O_499_48 = "0-499_48"
    UPDATED_AT = "updated_at"
    BUILT = "built"
    REGISTRATION_STATUS = "registration_status"
    PREDICTED_REGISTRATION = "predicted_registration"
    SCRAPER_TYPE = "scraper_type"
    
    
    def get(self,item):
        return item.value
    
    def get_name(self,item):
        return item.name

class Database:
  def __init__(self):
    self.host = os.environ.get("MYSQL_HOST")
    self.user = os.environ.get("MYSQL_USERNAME")
    self.password= os.environ.get("MYSQL_PASSWORD")
    self.database = os.environ.get("MYSQL_DATABASE")
    self.charset = "utf8"
    self.cursor = None

  def disconnect (self):
    self.db.close()

  def connect (self):
    # Open database connection
    self.db = pymysql.connect(host=self.host,user=self.user,password=self.password,database=self.database,cursorclass=pymysql.cursors.DictCursor)
    # #self.db.set_character_set(self.obj_config.charset)
    self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
    self.cursor.execute('SET NAMES ' + self.charset + ';')
    self.cursor.execute('SET CHARACTER SET ' + self.charset + ';')
    self.cursor.execute('SET character_set_connection=' + self.charset + ';')

  def recInsert (self,table,records):
    #conn = self.initDB()
    arr_values = []
    db_value=") VALUES ("  
    sql_qry=""

    for key in records :
      if ( records[key] != '' ):
        if isinstance(records[key],dict) and 'func' in records[key].keys():
            if sql_qry:
              sql_qry+=",`"+key+"`"
              db_value+=","+records[key]['func']
            else :
              sql_qry+="`"+key+"`"
              db_value+=records[key]['func']
        else:
            if sql_qry:
              sql_qry+=",`"+key+"`"
              db_value+=",%s"        
            else :
              sql_qry+=key+"`"
              db_value+="%s"            
            arr_values.append(records[key])
      
    
    sql_qry+=db_value+')'
    sql_qry="INSERT INTO "+table+"(`"+sql_qry    
    self.cursor.execute(sql_qry,arr_values)    
    self.db.commit()
    last_insert_id = self.cursor.lastrowid
    return last_insert_id
  
  def recSelect (self,table,where_dictionary=None,limit=None,order_by=None,order_type=None):
    #cursor = self.db.cursor(pymysql.cursors.DictCursor)
    
    sql_qry="SELECT * FROM "+table
    if where_dictionary:
        sql_qry += " WHERE "
    arr_values = []
    if where_dictionary:
      for key in where_dictionary:    
        if len(arr_values) > 0:      
          sql_qry+=" AND `"+key+"` = %s ";
        else:
          sql_qry+=' `'+key+"` = %s ";        
        arr_values.append(where_dictionary[key])
    if order_by:
      sql_qry+=" ORDER BY `"+order_by+"`"
      if order_type:      
        sql_qry+= " "+order_type+" "
    if limit:
      sql_qry+=" LIMIT "+str(limit)
    #print sql_qry
    self.cursor.execute(sql_qry,arr_values)
    result = self.cursor.fetchall()
    return result

  def recCustomQuery (self,sql_qry):
    #cursor = self.db.cursor(pymysql.cursors.DictCursor)
    
    self.cursor.execute(sql_qry)    
    m = re.match(r'select ', sql_qry,re.S|re.M|re.I)
    if m:      
      result = self.cursor.fetchall()
      return result
    self.db.commit()
    return []

  def recGetCount (self,table,where_dictionary):
    #cursor = self.db.cursor(pymysql.cursors.DictCursor)
    
    sql_qry="SELECT COUNT(*) as cnt FROM "+table+" WHERE "
    arr_values = []
    for key in where_dictionary:    
      if len(arr_values) > 0:      
        sql_qry+=" AND "+key+" = %s ";
      else:
        sql_qry+=key+" = %s ";        
      arr_values.append(where_dictionary[key])
    self.cursor.execute(sql_qry,arr_values)
    result = self.cursor.fetchall()
    return result[0]['cnt']

  def recUpdate (self,table,records,where_dictionary):
    #cursor = self.db.cursor(pymysql.cursors.DictCursor)
    arr_values = []
    
    rec_value_count = 0
    sql_qry = "";
    
    for key in records :
      if isinstance(records[key],dict) and 'func' in records[key].keys() :
        if sql_qry:
            sql_qry+=",`"+key+"`="+ records[key]['func']
        else:      
            sql_qry+="`"+key+"`="+ records[key]['func']          
      else:
          if sql_qry:
            sql_qry+=",`"+key+"` = %s"    
          else:      
            sql_qry+=key+" = %s"        
          arr_values.append(records[key])    
      rec_value_count += 1
    if ( rec_value_count == 0 ) :
      return 1;    
    for key in where_dictionary:  
      if((rec_value_count- len(records))>0):      
        sql_qry+=" AND `"+key+"` = %s "    
      else:      
        sql_qry+=" WHERE `"+key+"` = %s "          
      arr_values.append(where_dictionary[key])
      rec_value_count += 1

    sql_qry = "UPDATE " + table + " SET " + sql_qry
    #print sql_qry  
    self.cursor.execute(sql_qry,arr_values)  
    self.db.commit()
    #conn.close()
  def recInsertUpdate(self,table,records,where_dictionary):
      rec_count = self.recGetCount(table,where_dictionary)
      if rec_count:
        self.recUpdate(table,records,where_dictionary)
      else:
        return self.recInsert(table,records)
    
  
  def recDelete (self,table,where_dictionary):
    arr_values = []
    sql_qry = "DELETE FROM "+table;
    for key in where_dictionary:
        if len(arr_values)>0:
            sql_qry += " AND " + key + "=%s"
        else:
            sql_qry += " WHERE " + key + "=%s"
        arr_values.append(where_dictionary[key])
    
    self.cursor.execute(sql_qry,arr_values)
    self.db.commit()
  
  def getCurrentTs (self):
    self.cursor.execute( "SELECT NOW( ) AS current_ts" )
    result = self.cursor.fetchall()
    return result[0]['current_ts']


class DatabaseManager:
    def __init__(self) -> None:
      self.table = TableName()
      self.listings = Listings()
      self.status = Status()
      self.scraper_name = ScraperName()
      self.scraper_type = ScraperType()
      self.db = Database()