from sqlalchemy import Engine, MetaData, Table, insert, text

# feedsnooplyze modules
from feedsnooplyze.page import PageContent



class PersistenceCommand:
    def __init__(self, engine: Engine):
        self.engine = engine


    def add_content(self, page_name: str, content_time: str, content_hash: str, full_content : str, added_content: str):
        metadata = MetaData()
        
        table = Table('page_content', metadata, autoload_with=self.engine)

        sql = insert(table).values(
            page_name=page_name,
            content_time=content_time,
            content_hash=content_hash,
            full_content=full_content,
            added_content=added_content)

        with self.engine.connect() as conn:
            conn.execute(sql)
            conn.commit()


    def is_content_available(self, page_name : str) -> bool:
        sql = text("""
                SELECT 1 
                FROM page_content
                WHERE page_name = :page_name
                ORDER BY content_time DESC
                LIMIT 1
            """)
        
        
        with self.engine.connect() as conn:
            result = conn.execute(sql, {"page_name": page_name}).scalar()


        if result:
            return True
        else:
            return False



    def get_latest_by_name(self, page_name : str) -> PageContent:        
        sql = text("""
                SELECT page_name, content_time, content_hash, full_content, added_content
                FROM page_content
                WHERE page_name = :page_name
                ORDER BY content_time DESC
                LIMIT 1
            """)
        
        with self.engine.connect() as conn:
            result = conn.execute(sql, {"page_name": page_name}).fetchall()

        return PageContent(page_name=result[0][0], content_time=result[0][1], content_hash=result[0][2], full_content=result[0][3], added_content=result[0][4])
        
