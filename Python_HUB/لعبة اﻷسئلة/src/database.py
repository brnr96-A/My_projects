import sqlite3
import hashlib

def hash_password(password):
    """تشفير كلمة المرور بنظام SHA-256 لحمايتها"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    """إنشاء قاعدة البيانات وجدول المستخدمين إذا لم تكن موجودة"""
    conn = sqlite3.connect("quiz_game.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            high_score INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def check_user_login(username, password):
    """التحقق من صحة بيانات الدخول وإعادة (هل نجح، أعلى سكور)"""
    conn = sqlite3.connect("quiz_game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password, high_score FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row and row[0] == hash_password(password):
        return True, row[1]  # نجح الدخول، ويعيد أعلى سكور سابق
    return False, 0

def register_user(username, password):
    """إنشاء حساب مستخدم جديد في قاعدة البيانات"""
    hashed_pass = hash_password(password)
    try:
        conn = sqlite3.connect("quiz_game.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pass))
        conn.commit()
        conn.close()
        return True  # تم التسجيل بنجاح
    except sqlite3.IntegrityError:
        return False  # اسم المستخدم مسجل مسبقاً

def update_high_score(username, new_score):
    """تحديث الرقم القياسي للاعب"""
    conn = sqlite3.connect("quiz_game.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET high_score = ? WHERE username = ?", (new_score, username))
    conn.commit()
    conn.close()
