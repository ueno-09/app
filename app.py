from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# 共通のデータベース接続関数
def get_db_connection():
    conn = sqlite3.connect('practice_tracker.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- 画面1: ログイン・登録画面のHTML ---
AUTH_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>継続練習を目指すアプリ - 認証</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-gray-100 flex flex-col items-center justify-center min-h-screen p-4">
    <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 class="text-2xl font-bold mb-6 text-center text-gray-800">継続練習アプリ</h1>
        
        {% if error_message %}<div class="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded text-sm">{{ error_message }}</div>{% endif %}
        {% if success_message %}<div class="mb-4 bg-green-100 border border-green-400 text-green-700 px-4 py-2 rounded text-sm">{{ success_message }}</div>{% endif %}

        <div class="mb-8">
            <h2 class="text-lg font-semibold mb-3 text-gray-700">ログイン</h2>
            <form action="/login" method="POST" class="space-y-3">
                <div>
                    <label class="block text-sm text-gray-600">メールアドレス</label>
                    <input type="text" name="email" class="mt-1 block w-full rounded border border-gray-300 p-2" required>
                </div>
                <div>
                    <label class="block text-sm text-gray-600">パスワード</label>
                    <input type="password" name="password" class="mt-1 block w-full rounded border border-gray-300 p-2" required>
                </div>
                <button type="submit" class="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">ログイン</button>
            </form>
        </div>
        <hr class="border-gray-200 mb-6">
        <div>
            <h2 class="text-lg font-semibold mb-3 text-gray-700">アカウント新規登録</h2>
            <form action="/register" method="POST" class="space-y-3">
                <div>
                    <label class="block text-sm text-gray-600">メールアドレス</label>
                    <input type="text" name="email" class="mt-1 block w-full rounded border border-gray-300 p-2" required>
                </div>
                <div>
                    <label class="block text-sm text-gray-600">パスワード</label>
                    <input type="password" name="password" class="mt-1 block w-full rounded border border-gray-300 p-2" required>
                </div>
                <button type="submit" class="w-full bg-green-500 text-white p-2 rounded hover:bg-green-600">新規登録</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

# --- 画面2: タイマー・記録画面のHTML ---
TIMER_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>継続練習を目指すアプリ - タイマー</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-gray-100 min-h-screen p-6">
    <div class="max-w-md mx-auto bg-white p-8 rounded-lg shadow-md text-center">
        <h1 class="text-xl font-bold text-gray-800 mb-2">練習タイマー画面</h1>
        <p class="text-sm text-gray-500 mb-6">ログイン中: {{ email }}</p>

        <div class="text-5xl font-mono font-bold text-blue-600 my-8" id="timerDisplay">00:00:00</div>

        <div class="flex justify-center space-x-4 mb-8">
            <button id="startBtn" onclick="startTimer()" class="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600">スタート</button>
            <button id="pauseBtn" onclick="pauseTimer()" class="bg-yellow-500 text-white px-6 py-2 rounded hover:bg-yellow-600 hidden">一時停止</button>
            <button id="startBtn2" onclick="startTimer()" class="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 hidden">再開</button>
            <button id="stopBtn" onclick="stopTimer()" class="bg-red-500 text-white px-6 py-2 rounded hover:bg-red-600 hidden">ストップ</button>
        </div>

        <form action="/save_session" method="POST" id="saveForm" class="hidden border-t pt-6 space-y-4 text-left">
            <input type="hidden" name="user_id" value="{{ user_id }}">
            <input type="hidden" name="email" value="{{ email }}">
            <input type="hidden" name="duration" id="durationInput">

            <div>
                <label class="block text-sm font-medium text-gray-700">計測結果（秒）</label>
                <input type="text" id="durationDisplay" class="mt-1 block w-full bg-gray-100 border p-2 rounded" readonly>
            </div>
            <div>
                <label class="block text-sm font-medium text-gray-700">練習日（自動記録）</label>
                <input type="text" name="date" value="{{ today }}" class="mt-1 block w-full bg-gray-100 border p-2 rounded" readonly>
            </div>
            
            <button type="submit" class="w-full bg-green-500 text-white p-3 rounded font-bold hover:bg-green-600">
                この内容で練習を記録する
            </button>
        </form>
    </div>

    <script>
        let timer = null;
        let seconds = 0;

        function updateDisplay() {
            let hrs = Math.floor(seconds / 3600).toString().padStart(2, '0');
            let mins = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
            let secs = (seconds % 60).toString().padStart(2, '0');
            document.getElementById('timerDisplay').innerText = `${hrs}:${mins}:${secs}`;
        }

        function startTimer() {
            if (timer === null) {
                timer = setInterval(() => { seconds++; updateDisplay(); }, 1000);
                document.getElementById('startBtn').classList.add('hidden');
                document.getElementById('startBtn2').classList.add('hidden');
                document.getElementById('pauseBtn').classList.remove('hidden');
                document.getElementById('stopBtn').classList.remove('hidden');
            }
        }

        function pauseTimer() {
            clearInterval(timer);
            timer = null;
            document.getElementById('startBtn2').classList.remove('hidden');
            document.getElementById('pauseBtn').classList.add('hidden');
        }

        function stopTimer() {
            clearInterval(timer);
            timer = null;
            
            // ユーザー入力・結果の検証（0秒の時はエラーとして扱うバリデーション）
            if (seconds === 0) {
                alert("練習時間が0秒のため、記録できません。");
                location.reload();
                return;
            }

            // フォームに値をセットして表示
            document.getElementById('durationInput').value = seconds;
            document.getElementById('durationDisplay').value = seconds + " 秒";
            document.getElementById('saveForm').classList.remove('hidden');
            
            // ボタンの無効化
            document.getElementById('startBtn').classList.add('hidden');
            document.getElementById('startBtn2').classList.add('hidden');
            document.getElementById('pauseBtn').classList.add('hidden');
            document.getElementById('stopBtn').classList.add('hidden');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(AUTH_TEMPLATE)

# 新規登録の処理
@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    if not email or not password or "@" not in email:
        return render_template_string(AUTH_TEMPLATE, error_message="登録内容が正しくありません。")
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
        conn.commit()
    except sqlite3.IntegrityError:
        return render_template_string(AUTH_TEMPLATE, error_message="既に登録されているメールアドレスです。")
    finally:
        conn.close()
    return render_template_string(AUTH_TEMPLATE, success_message="登録完了！ログインしてください。")

# ログインの処理
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
    conn.close()

    if user is None:
        return render_template_string(AUTH_TEMPLATE, error_message="メールアドレスまたはパスワードが間違っています。")

    # 認証成功時、タイマー画面へ遷移（データを渡す）
    today_str = datetime.now().strftime('%Y-%m-%d')
    return render_template_string(TIMER_TEMPLATE, email=user['email'], user_id=user['user_id'], today=today_str)

# 練習セッションの保存処理
@app.route('/save_session', methods=['POST'])
def save_session():
    user_id = request.form.get('user_id')
    email = request.form.get('email')
    duration = request.form.get('duration')
    date_str = request.form.get('date')

    # 【入力検証】
    if not duration or int(duration) <= 0:
        return "エラー: 計測時間が不正です。", 400

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO practice_sessions (user_id, practice_date, duration_seconds) 
        VALUES (?, ?, ?)
    ''', (user_id, date_str, int(duration)))
    conn.commit()
    
    # これまでの全データを取得
    all_sessions = conn.execute('SELECT * FROM practice_sessions WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()

    # 記録完了画面（簡易表示）
    history = "<br>".join([f"日付: {s['practice_date']} | 時間: {s['duration_seconds']}秒" for s in all_sessions])
    return f"<h3>ユーザー {email} さんの練習記録を保存しました！</h3><p>【これまでの履歴】</p>{history}<br><br><a href='/'>ログアウト（ホームへ）</a>"

if __name__ == '__main__':
    app.run(debug=True)