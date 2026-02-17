import psycopg2 
from psycopg2 import errors
import bcrypt
import pandas as pd

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgresql"
    )

def create_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    from random import randint
    id = randint(1, 2**12-1)
    hashed_passwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute(
            """
            INSERT INTO users (user_id, email, password_hash)
            VALUES (%s, %s, %s)
            """,
            (id, email, hashed_passwd.decode("utf-8"))
        )
        conn.commit()
        return True, f"User with email {email} created successfully"

    except errors.UniqueViolation:
        conn.rollback()
        return False, f"User with email {email} already exists"

    finally:
        cursor.close()
        conn.close()


def authenticate_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password_hash FROM users WHERE email = %s",
        (email,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        stored_hash = result[0].encode("utf-8")
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            return True
    return False


def fetch_feeds(limit=20) -> pd.DataFrame:
    conn = get_connection()
    query = f"""
        SELECT rss_name, rss_feed_name, title, link, published, summary
        FROM rss_feed_content
        ORDER BY published DESC
        LIMIT {limit};
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


#def get_available_topics():
#    conn = get_connection()
#    cursor = conn.cursor()
#    cursor.execute("SELECT name FROM topics ORDER BY name ASC")
#    rows = cursor.fetchall()
#    conn.close()
#    return [row[0] for row in rows]


def get_available_topics():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, color, icon FROM topics ORDER BY name ASC")
    rows = cursor.fetchall()
    conn.close()

    # Convert to dictionary
    topics_dict = {}
    for row in rows:
        name, color, icon = row
        topics_dict[name] = {"color": color, "icon": icon}

    return topics_dict


def save_user_topics(user_email, selected_topics, name, surname):
    conn = get_connection()
    cursor = conn.cursor()

    # Get user id
    cursor.execute("SELECT user_id FROM users WHERE email = %s", (user_email,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        raise ValueError(f"No user found with email {user_email}")
    user_id = result[0]

    # Optional: delete existing topics first
    cursor.execute("DELETE FROM user_topics WHERE user_id = %s", (user_id,))

    # Insert selected topics
    for topic_name in selected_topics:
        # Get topic_id
        cursor.execute("SELECT topic_id FROM topics WHERE name = %s", (topic_name,))
        topic_row = cursor.fetchone()
        if topic_row:
            topic_id = topic_row[0]
            cursor.execute(
                "INSERT INTO user_topics (user_id, topic_id) VALUES (%s, %s)",
                (user_id, topic_id)
            )

    # Mark user as customized
    cursor.execute("UPDATE users SET needs_customization = FALSE, name = %s, surname = %s WHERE user_id = %s", (name, surname, user_id,))

    conn.commit()
    conn.close()