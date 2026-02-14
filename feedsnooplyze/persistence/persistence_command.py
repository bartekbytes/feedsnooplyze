from sqlalchemy import Engine, MetaData, Table, Column, String, DateTime, Text, insert, text, select, desc, bindparam

# feedsnooplyze modules
from feedsnooplyze.sourcer.page import PageContent
from feedsnooplyze.sourcer.rss import RSSContent
from feedsnooplyze.sourcer.rss import RSSFeedContent


class PersistenceCommand:
    def __init__(self, engine: Engine):
        self.engine = engine


    def add_page_content(self, page_name: str, content_time: str, content_hash: str, full_content : str, added_content: str):
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

    def add_rss_content(self, rss_name: str, content_time: str, content_hash: str,
                        full_content : str, added_content: str):
        
        metadata = MetaData()
        
        table = Table('rss_content', metadata, autoload_with=self.engine)

        sql = insert(table).values(
            rss_name=rss_name,
            content_time=content_time,
            content_hash=content_hash,
            full_content=str(full_content),
            added_content=str(added_content)
            )

        with self.engine.connect() as conn:
            conn.execute(sql)
            conn.commit()


    def add_rss_feed_content(self, rss_name: str, rss_feed_name: str, content_time: str, 
                        content_hash: str, full_content : str, added_content: str,
                        title: str, link: str, published: str, summary: str):
        
        metadata = MetaData()
        
        table = Table('rss_feed_content', metadata, autoload_with=self.engine)

        sql = insert(table).values(
            rss_name=rss_name,
            rss_feed_name=rss_feed_name,
            content_time=content_time,
            content_hash=content_hash,
            full_content=str(full_content),
            added_content=str(added_content),
            title = title,
            link = link,
            published = published,
            summary = summary
            )

        with self.engine.connect() as conn:
            conn.execute(sql)
            conn.commit()


    def is_content_available(self, sourcer_type: str, object_name : str) -> bool:        

        metadata = MetaData()

        if sourcer_type == "page":

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
                .where(page_content.c.page_name == bindparam("object_name"))
                .order_by(desc(page_content.c.content_time))
                .limit(1)
            )
        
            with self.engine.connect() as conn:
                result = conn.execute(sql, {"object_name": object_name}).fetchone()

            if result:
                return True
            else:
                return False
            
        elif sourcer_type == "rss":
             
            rss_content = Table(
                'rss_content', metadata,
                Column('rss_name', String(100), nullable=False),
                Column('content_time', DateTime, nullable=False),
                Column('content_hash', String(100), nullable=False),
                Column('full_content', Text),
                Column('added_content', Text)
            )

            sql = (
                select(1)
                .where(rss_content.c.rss_name == bindparam("object_name"))
                .order_by(desc(rss_content.c.content_time))
                .limit(1)
            )
        
            with self.engine.connect() as conn:
                result = conn.execute(sql, {"object_name": object_name}).fetchone()

            if result:
                return True
            else:
                return False

        elif sourcer_type == "rssfeed":
             
            rss_feed_content = Table(
                'rss_feed_content', metadata,
                Column('rss_name', String(100), nullable=False),
                Column('rss_feed_name', String(100), nullable=False),
                Column('content_time', DateTime, nullable=False),
                Column('content_hash', String(100), nullable=False),
                Column('full_content', Text),
                Column('added_content', Text),
                Column('title', String(200), nullable=False),
                Column('link', String(100), nullable=False),
                Column('published', String(100), nullable=False),
                Column('summary', Text, nullable=False)
            )

            sql = (
                select(1)
                .where(rss_feed_content.c.rss_feed_name == bindparam("object_name"))
                .order_by(desc(rss_feed_content.c.content_time))
                .limit(1)
            )
        
            with self.engine.connect() as conn:
                result = conn.execute(sql, {"object_name": object_name}).fetchone()

            if result:
                return True
            else:
                return False



    def get_latest_by_name(self, sourcer_type: str, object_name : str) -> PageContent | RSSContent:
        
        metadata = MetaData()

        if sourcer_type == "page":
        
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
                .where(page_content.c.page_name == bindparam("object_name"))
                .order_by(desc(page_content.c.content_time))
                .limit(1)
            )
        
            with self.engine.connect() as conn:
                result = conn.execute(sql, {"object_name": object_name}).fetchone()

            return PageContent(page_name=result[0], content_time=result[1], content_hash=result[2], full_content=result[3], added_content=result[4])
        
        elif sourcer_type == "rss":

            rss_content = Table(
                'rss_content', metadata,
                Column('rss_name', String(100), nullable=False),
                Column('content_time', DateTime, nullable=False),
                Column('content_hash', String(100), nullable=False),
                Column('full_content', Text),
                Column('added_content', Text)
            )

            sql = (
                select(
                    rss_content.c.rss_name,
                    rss_content.c.content_time,
                    rss_content.c.content_hash,
                    rss_content.c.full_content,
                    rss_content.c.added_content,
                )
                .where(rss_content.c.rss_name == bindparam("object_name"))
                .order_by(desc(rss_content.c.content_time))
                .limit(1)
            )
        
            with self.engine.connect() as conn:
                result = conn.execute(sql, {"object_name": object_name}).fetchone()

            return RSSContent(
                    rss_name=result[0], content_time=result[1], content_hash=result[2],
                    full_content=result[3], added_content=result[4])

        elif sourcer_type == "rssfeed":

            rss_feed_content = Table(
                'rss_feed_content', metadata,
                Column('rss_name', String(100), nullable=False),
                Column('rss_feed_name', String(100), nullable=False),
                Column('content_time', DateTime, nullable=False),
                Column('content_hash', String(100), nullable=False),
                Column('full_content', Text),
                Column('added_content', Text),
                Column('title', String(200), nullable=False),
                Column('link', String(100), nullable=False),
                Column('published', String(100), nullable=False),
                Column('summary', Text, nullable=False)
            )

            sql = (
                select(
                    rss_feed_content.c.rss_name,
                    rss_feed_content.c.rss_feed_name,
                    rss_feed_content.c.content_time,
                    rss_feed_content.c.content_hash,
                    rss_feed_content.c.full_content,
                    rss_feed_content.c.added_content,
                    rss_feed_content.c.title,
                    rss_feed_content.c.link,
                    rss_feed_content.c.published,
                    rss_feed_content.c.summary,
                )
                .where(rss_feed_content.c.rss_feed_name == bindparam("object_name"))
                .order_by(desc(rss_feed_content.c.content_time))
                .limit(1)
            )
        
            with self.engine.connect() as conn:
                result = conn.execute(sql, {"object_name": object_name}).fetchone()

            return RSSFeedContent(
                    rss_name=result[0], rss_feed_name=result[1], content_time=result[2], content_hash=result[3],
                    full_content=result[4], added_content=result[5],
                    title=result[6], link=result[7], published=result[8], summary=result[9]
                )