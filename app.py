import os
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "credit_card.db")


def init_db():
    """建立資料庫與資料表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_name TEXT,
            bank_name TEXT,
            billing_date INTEGER,
            due_date INTEGER
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id INTEGER,
            billing_month TEXT,
            amount REAL,
            is_paid INTEGER DEFAULT 0,
            FOREIGN KEY(card_id) REFERENCES cards(id)
        )
    """
    )
    conn.commit()
    conn.close()


@app.route("/")
def home():
    return jsonify(
        {
            "status": "success",
            "message": "信用卡繳費管理系統功能升級版已就緒！",
        }
    )


# ==================== 功能一：新增信用卡 ====================
@app.route("/api/add_card", methods=["POST"])
def add_card():
    data = request.get_json()
    card_name = data.get("card_name")
    bank_name = data.get("bank_name")
    billing_date = data.get("billing_date")  # 結帳日 (例如: 10)
    due_date = data.get("due_date")  # 繳款截止日 (例如: 25)

    if not card_name or not bank_name:
        return jsonify({"status": "error", "message": "請輸入卡片與銀行名稱"}), 400

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cards (card_name, bank_name, billing_date, due_date) VALUES (?, ?, ?, ?)",
        (card_name, bank_name, billing_date, due_date),
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": f"成功新增信用卡：{card_name}"})


# ==================== 功能二：查詢所有信用卡 ====================
@app.route("/api/get_cards", methods=["GET"])
def get_cards():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cards")
    rows = cursor.fetchall()
    conn.close()

    cards_list = []
    for row in rows:
        cards_list.append(
            {
                "id": row[0],
                "card_name": row[1],
                "bank_name": row[2],
                "billing_date": row[3],
                "due_date": row[4],
            }
        )

    return jsonify({"status": "success", "cards": cards_list})


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
