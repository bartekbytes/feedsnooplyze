from sqlalchemy import Engine, MetaData, Table, Column, String, DateTime, Text, insert, text, select, desc, bindparam

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

        metadata = MetaData()

        page_content = Table(
            'page_content', metadata,
            Column('page_name', String(100), nullable=False),
            Column('content_time', DateTime, nullable=False),
            Column('content_hash', String(100), nullable=False),
            Column('full_content', Text),
            Column('added_content', Text)
        )

        sql = (
            select(1)
            .where(page_content.c.page_name == bindparam("page_name"))
            .order_by(desc(page_content.c.content_time))
            .limit(1)
        )
        
        with self.engine.connect() as conn:
            result = conn.execute(sql, {"page_name": page_name}).fetchone()

        if result:
            return True
        else:
            return False



    def get_latest_by_name(self, page_name : str) -> PageContent:                
        
        metadata = MetaData()

        page_content = Table(
            'page_content', metadata,
            Column('page_name', String(100), nullable=False),
            Column('content_time', DateTime, nullable=False),
            Column('content_hash', String(100), nullable=False),
            Column('full_content', Text),
            Column('added_content', Text)
        )

        sql = (
            select(
                page_content.c.page_name,
                page_content.c.content_time,
                page_content.c.content_hash,
                page_content.c.full_content,
                page_content.c.added_content,
            )
            .where(page_content.c.page_name == bindparam("page_name"))
            .order_by(desc(page_content.c.content_time))
            .limit(1)
        )
        
        with self.engine.connect() as conn:
            result = conn.execute(sql, {"page_name": page_name}).fetchone()

        return PageContent(page_name=result[0], content_time=result[1], content_hash=result[2], full_content=result[3], added_content=result[4])
        
