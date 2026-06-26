import sqlite3

def init_database():
    conn = sqlite3.connect('practice_tracker.db')
    cursor = conn.cursor()
    
    # ユーザーテーブルの作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # 練習記録テーブルの作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS practice_sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            practice_date DATE NOT NULL,
            duration_seconds INTEGER NOT NULL,
            attached_file_path TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("データベースの更新が完了しました。（練習記録テーブルの追加）")

if __name__ == '__main__':
    init_database()