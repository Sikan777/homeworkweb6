import logging  # Імпорт модуля для логування

import faker  # Імпорт бібліотеки faker щоб не було підкреслень
#from faker import Faker  # Імпорт класу Faker для генерації випадкових даних
import random  # Імпорт модуля для генерації випадкових чисел
import psycopg2  # Імпорт модуля для взаємодії з PostgreSQL базою даних

fake = faker.Faker()  # Створення екземпляру класу Faker для генерації фейкових даних

def execute_sql_from_file(filename, cursor):
    # Функція для виконання SQL-запитів з файлу, переданого у параметрі filename, за допомогою курсора cursor
    with open(filename, 'r') as file:
        sql_query = file.read()
        cursor.execute(sql_query)

def main():
    try:
        # Встановлення з'єднання з PostgreSQL базою даних
        conn = psycopg2.connect(host="5432", database="postgres", user="postgres", password="mysecretpassword")
        cur = conn.cursor()  # Створення курсора для взаємодії з базою даних

        """ Додавання даних до таблиць """

        for _ in range(3):
            cur.execute("INSERT INTO groups (name) VALUES (%s)", (fake.word(),))

        for _ in range(3):
            cur.execute("INSERT INTO teachers (fullname) VALUES (%s)", (fake.name(),))

        for teacher_id in range(1, 4):
            for _ in range(2):
                cur.execute("INSERT INTO subjects (name, teacher_id) VALUES (%s, %s)", (fake.word(), teacher_id))

        for group_id in range(1, 4):
            for _ in range(10):
                cur.execute("INSERT INTO students (fullname, group_id) VALUES (%s, %s) RETURNING id",
                            (fake.name(), group_id))
                student_id = cur.fetchone()[0]
                for subject_id in range(1, 7):
                    for _ in range(3):
                        cur.execute(
                            "INSERT INTO grades (student_id, subject_id, grade, grade_date) VALUES (%s, %s, %s, %s)",
                            (student_id, subject_id, random.randint(0, 50), fake.date_this_decade()))

        """ Виконання SQL-запитів з файлів """
        query_files = ['query1.sql', 'query2.sql', 'query3.sql', 'query4.sql', 'query5.sql', 'query6.sql',
                       'query7.sql', 'query8.sql', 'query9.sql', 'query10.sql']
        for file in query_files:
            execute_sql_from_file(file, cur)  # Виклик функції для виконання SQL-запиту з файлу
            result = cur.fetchall()
            print(f"Result for '{file}': {result}")

        conn.commit()  # Підтвердження транзакції

    except psycopg2.Error as e:
        logging.error(e)  # Логування помилок у випадку виникнення винятку
        conn.rollback()  # Скасування транзакції у випадку помилки
    finally:
        if conn is not None:
            conn.close()  # Закриття з'єднання з базою даних у будь-якому випадку

if __name__ == "__main__":
    main()  # Виклик головної функції, яка виконує основний логіку програми
