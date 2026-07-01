import os
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

# 自動取得這個檔案在 Windows 電腦上的實際資料夾路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "credit_card.db")

def init_db():
    """初始化 SQLite 資料庫，建立信用卡與帳單資料表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. 建立信用卡表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_name TEXT,
            bank_name TEXT,
            billing_date INTEGER,
            due_date INTEGER
        )
    """)

    # 2. 建立帳單管理表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id INTEGER,
            billing_month TEXT,
            amount REAL,
            is_paid INTEGER DEFAULT 0,
            FOREIGN KEY(card_id) REFERENCES cards(id)
        )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "信用卡繳費管理系統後端已在您的 Windows 電腦成功啟動！"
    })

if __name__ == "__main__":
    init_db()  # 啟動時自動檢查並建立 credit_card.db 檔案
    # 電腦開發測試，開啟 debug=True，這樣改程式會自動重啟
    app.run(host="127.0.0.1", port=5000, debug=True)
