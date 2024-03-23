import psycopg2


class JobOffersDB:
    def __init__(self, database_name, database_user, database_password, database_host, database_port, table_name):
        self.database_name = database_name
        self.database_user = database_user
        self.database_password = database_password
        self.database_host = database_host
        self.database_port = database_port
        self.table_name = table_name

    def insert_job_offer(self, data):
        try:
            conn = psycopg2.connect(
                dbname=self.database_name,
                user=self.database_user,
                password=self.database_password,
                host=self.database_host,
                port=self.database_port
            )
            cursor = conn.cursor()

            insert_query = f"""
                    INSERT INTO {self.table_name} (title, company, type_of_work, experience, employment_type, 
                    operating_mode, stack, earnings_from, earnings_to) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_query, data)
            conn.commit()
            cursor.close()
            conn.close()

            print("Data inserted successfully.")
        except psycopg2.Error as e:
            print(f"Error inserting data: {e}")
