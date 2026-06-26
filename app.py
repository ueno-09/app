from flask import Flask, render_template_string, request

app = Flask(__name__)

# シンプルなHTMLテンプレート（Tailwind CSSを読み込み）
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>継続練習を目指すアプリ</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-gray-100 flex items-center justify-center h-screen">
    <div class="bg-white p-8 rounded-lg shadow-md w-96">
        <h1 class="text-xl font-bold mb-4 text-center">継続練習アプリ（開発中）</h1>
        
        <form action="/login" method="POST" class="space-y-4">
            <div>
                <label class="block text-sm font-medium text-gray-700">メールアドレス</label>
                <input type="text" name="email" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2 focus:ring-blue-500 focus:border-blue-500">
            </div>
            
            {% if error_message %}
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded text-sm">
                {{ error_message }}
            </div>
            {% endif %}
            
            <button type="submit" class="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition">
                ログイン（入力チェックテスト）
            </button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    # 4. ユーザ入力の検証（バリデーション）
    email = request.form.get('email', '').strip()
    
    # 簡易エラーチェック（未入力、または@が含まれていない場合）
    if not email:
        return render_template_string(HTML_TEMPLATE, error_message="メールアドレスを入力してください。")
    elif "@" not in email:
        return render_template_string(HTML_TEMPLATE, error_message="有効なメールアドレスの形式ではありません。")
    
    # 検証を通過した場合（次のステップへの土台）
    return f"ログイン成功（デバッグ用）: {email} さん、こんにちは！"

if __name__ == '__main__':
    # 開発用サーバーを起動
    app.run(debug=True)