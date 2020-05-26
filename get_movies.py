import scraping
import psycopg2
import psycopg2.extras


try:
    connection = psycopg2.connect(user = "postgres", password = "panacotta", host = "127.0.0.1", port = "5432", database = "films")
    cursor = connection.cursor()
    print(connection.get_dsn_parameters(),"\n")

    cursor.execute("DROP TABLE IF EXISTS movies;")
    connection.commit()
    cursor.execute("""CREATE TABLE movies (
        ALLOCINE_ID INT PRIMARY KEY,
        TITLE VARCHAR(150),
        RELEASE VARCHAR(50),
        GENRES VARCHAR(150),
        DIRECTORS VARCHAR(150),
        PRESS_RATING NUMERIC(2,1),
        PUB_RATING NUMERIC(2,1));
        """)
    connection.commit()
    
    df = scraping.df
    if len(df) > 0:
        df_columns = list(df)
        columns = ",".join(df_columns)
        values = "VALUES ({})".format(",".join(["%s" for _ in df_columns])) # create string "VALUES(%s,%s,%s,%s,%s,%s,%s)"
        insert_stmt = "INSERT INTO movies ({}) {}".format(columns, values)
        psycopg2.extras.execute_batch(cursor, insert_stmt, df.values)
        # inserted = cursor.fetchall()
        # print("Inserted:", inserted,"\n")
        connection.commit()
        print("OK")


except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)

finally:
    print("Finally")

    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")