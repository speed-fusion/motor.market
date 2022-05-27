import sys

sys.path.append("/libs")

from Database import Database

from pulsar_manager import PulsarManager

from database_manager import DatabaseManager

import traceback

class topicHandler:
    def __init__(self):
        print("topic handler init")
        
        pulsar_manager = PulsarManager()
        
        self.database_manager = DatabaseManager()
        
        self.listings = self.database_manager.listings
        
        self.table = self.database_manager.table
        
        self.status = self.database_manager.status
        
        self.topics = pulsar_manager.topics
        
        self.logs_producer = pulsar_manager.create_producer(pulsar_manager.topics.LOGS)
        
        self.fl_listings_find_consumer = pulsar_manager.create_consumer(pulsar_manager.topics.FL_LISTINGS_FIND)
        
        self.producer = pulsar_manager.create_producer(pulsar_manager.topics.AUTOTRADER_LISTING_SCRAPER)
        
        self.at_urls_update_producer = pulsar_manager.create_producer(self.topics.AT_URLS_UPDATE)
        
        self.db = self.database_manager.db
        
    def handle_find_event(self,data):
        cn_scraper_name = self.listings.SCRAPER_NAME.value
        cn_source_id = self.listings.SOURCE_ID.value
        cn_id = self.listings.ID.value
        cn_dealer_id = self.listings.DEALER_ID.value
        cn_status = self.listings.STATUS.value
        cn_predicted_make = self.listings.PREDICTED_MAKE.value
        cn_predicted_model = self.listings.PREDICTED_MODEL.value
        cn_engine_cylinder_cc = self.listings.ENGINE_CYLINDER_CC.value
        cn_mileage = self.listings.MILEAGE.value
        cn_built = self.listings.BUILT.value
        cn_registration_status = self.listings.REGISTRATION_STATUS.value
        cn_predicted_registration = self.listings.PREDICTED_REGISTRATION.value
        cn_scraper_type = self.listings.SCRAPER_TYPE.value
        
        cv_sold = self.status.SOLD.value
        cv_manual_expire = self.status.MANUAL_EXPIRE.value
        cv_pending = self.status.PENDING.value
        cv_approval = self.status.APPROVAL.value
        cv_to_parse = self.status.TO_PARSE.value
        cv_url_scraper = self.database_manager.scraper_name.URL_SCRAPER.value
        cv_validator = self.database_manager.scraper_type.VALIDATOR.value
        cv_normal = self.database_manager.scraper_type.NORMAL.value
        
        tn_listings = self.table.LISTINGS.value
        
        
        self.db.connect()
        
        source_id = data["data"].get(cn_source_id)
        
        scraper_name = data["data"].get(cn_scraper_name,None)

        try:
            
            result = self.db.recCustomQuery(f'SELECT {cn_id},{cn_dealer_id},{cn_status},{cn_predicted_make},{cn_predicted_model},{cn_engine_cylinder_cc},{cn_mileage},{cn_built},{cn_registration_status},{cn_predicted_registration} FROM {tn_listings} WHERE {cn_source_id}="{source_id}"')
            
            if len(result) > 0:
                
                if scraper_name == cv_url_scraper:
                    what = {
                        "listing_id":result[0][cn_id],
                        "listing_status":result[0][cn_status],
                        "scraped":1,
                        "updated_at":{
                            "func":"now()"
                        },
                        "errorMessage":"listing already exists."
                    }
                    
                    if result[0][cn_status] == self.database_manager.status.PENDING.value:
                        what["number_plate_flag"] = 2
                    
                    where = {
                        "id":data["data"].get("listingId")
                    }
                    
                    # self.at_urls_update_producer.produce_message({
                    #     "data":{
                    #         "what":what,
                    #         "where":where
                    #     }
                    # })
                    
                
                
                
                if result[0][cn_status] in [cv_sold,cv_manual_expire,cv_pending,cv_approval,cv_to_parse]:
                    return
                
                data["data"][cn_scraper_type] = cv_validator
                
                data["data"].update(result[0])
            else:
                data["data"][cn_scraper_type] = cv_normal
            
            self.producer.produce_message(data)
            
        except Exception as e:
            print(f'error : {str(e)}')
        
        self.db.disconnect()
        
    def main(self):
        
        while True:
            try:
                message =  self.fl_listings_find_consumer.consume_message()
                
                skip_find = message["data"].get("skip_find",False)
                
                if skip_find == True:
                    self.producer.produce_message(message)
                    continue
                    
                
                source_url = message["data"].get("source_url")
                
                print(f'processing : {source_url}')
                
                self.handle_find_event(message)
                
                

            except Exception as e:
                print(f'error : {str(e)}')
                
                log = {}
                
                log["source_url"] = source_url
                
                log["service"] = self.topics.FL_LISTINGS_FIND.value
                
                log["error_message"] = traceback.format_exc()
                
                self.logs_producer.produce_message({
                    "eventType":"insertLog",
                    "data":log
                })

if __name__ == "__main__":
    th = topicHandler()
    th.main()