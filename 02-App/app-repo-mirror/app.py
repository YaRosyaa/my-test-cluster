from flask import Flask, render_template, request, redirect, url_for
from prometheus_flask_exporter import PrometheusMetrics
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Конфигурация БД из переменных окружения
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'db'),
    'database': os.environ.get('DB_NAME', 'task_manager'),
    'user': os.environ.get('DB_USER', 'taskuser'),
    'password': os.environ.get('DB_PASSWORD', 'StrongPassword123!')
}

def get_db_connection():
    """Создание подключения к базе данных"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    connection = get_db_connection()
    
    if request.method == 'POST':
        task_name = request.form.get('task_name', '').strip()
        if task_name and connection:
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO tasks (task_name) VALUES (%s)", (task_name,))
                connection.commit()
                cursor.close()
            except Error as e:
                print(f"Ошибка добавления задачи: {e}")
            finally:
                connection.close()
        return redirect(url_for('index'))
    
    tasks = []
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
            tasks = cursor.fetchall()
            cursor.close()
        except Error as e:
            print(f"Ошибка получения задач: {e}")
        finally:
            connection.close()
    
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            connection.commit()
            cursor.close()
        except Error as e:
            print(f"Ошибка удаления задачи: {e}")
        finally:
            connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
