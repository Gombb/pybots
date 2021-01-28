from psycopg2.extras import RealDictCursor
import database_common

@database_common.connection_handler
def insert_new_user(cursor, user_data):
    cursor.execute("""
                    INSERT INTO user_data
                    (username, pw_hash)
                    VALUES (%s, %s);
                    """,
                   (user_data["username"], user_data["password_hash"]))


@database_common.connection_handler
def get_password_hash(cursor):
    cursor.execute("""
                    SELECT pw_hash
                    FROM user_data
                    WHERE username = 'admin'
                    """)
    records = cursor.fetchone()
    return records["pw_hash"]


@database_common.connection_handler
def insert_new_trade_to_history(cursor, trade_data):
    cursor.execute("""
                    INSERT INTO trade_history
                    (side, time, strat, exec_price, order_type, quantity)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                   (trade_data["side"], trade_data["time"], trade_data["strat"], trade_data["exec_price"], trade_data["order_type"], trade_data["quantity"]))
