from environs import Env
from pymysql import connect, cursors, IntegrityError

env = Env()
env.read_env()

DB_NAME = env.str("DB_NAME")
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_PORT = env.int("DB_PORT")
DB_HOST = env.str("DB_HOST")

def execute(sql: str, params: tuple = (), fetchone = False, fetchall = False) -> dict | None:
    connection = connect(
        db=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        host=DB_HOST,
        cursorclass=cursors.DictCursor
    )
    cursor = connection.cursor()
    cursor.execute(sql, params)

    data = None

    if fetchone:
        data = cursor.fetchone()
    elif fetchall:
        data = cursor.fetchall()

    connection.commit()
    connection.close()

    return data


def register_user(telegram_id: str, fullname: str) -> None:
    sql = """
        INSERT INTO users(telegram_id, fullname)
        VALUES (%s, %s)
    """
    execute(sql, (telegram_id, fullname))


def get_user(telegram_id: str) -> dict | None:
    sql = """
        SELECT * FROM users WHERE telegram_id = %s
    """
    user = execute(sql, (telegram_id,), fetchone=True)
    return user


def register_city(telegram_id: str, city_name: str) -> None:
    user = get_user(telegram_id)

    if user:
        user_id = user.get("id")

        try:
            sql = """
                INSERT INTO cities(user, name)
                VALUES (%s, %s)
            """
            execute(sql, (user_id, city_name))
        except IntegrityError:
            ...


def get_user_cities(telegram_id: str) -> list:
    user = get_user(telegram_id=telegram_id)

    if user:
        user_id = user.get("id")
        sql = """
            SELECT name FROM cities WHERE user = %s
        """
        results = execute(sql, (user_id,), fetchall=True)
        cities = []

        for result in results:
            cities.append(result.get("name"))

        return cities
    else:
        return []


def clear_user_cities(telegram_id: str) -> None:
    user = get_user(telegram_id=telegram_id)

    if user:
        user_id = user.get("id")
        sql = """
            DELETE FROM cities WHERE user = %s
        """
        execute(sql, (user_id,))
