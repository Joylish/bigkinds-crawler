# BigKindsCrawler

사용 라이브러리
  - selenium
  - time,sleep
  - sys
  - re
  - csv
  - pandas
  - chromedriver
  - pymongo
  
DB 환경
  - mongoDB
  - pymongo 라이브러리
  - client = MongoClient() 로 디폴트 호스트와 포트에 연결
  - db = client["bigkinds_db"] 로 빅카인즈db 생성
  - collection = db["bigkinds_collection"] 으로 collection 생성
  - values = {"id":id,
                          "category":category,
                          "title":title,
                          "written_at":written_at,
                          "content":content}
     values_id = collection.insert_one(values)
     위 코드로 json형태로 collection에 insert
