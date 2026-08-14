import sys
import os
import random
import sqlite3
import hashlib
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QMessageBox, QLineEdit)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon, QFont

import arabic_reshaper

# =====================================================================
# 1. دالات معالجة النصوص وحماية البيانات
# =====================================================================
def fix_arabic(text):
    """دالة لضمان اتصال الحروف العربية بشكل صحيح في أنظمة اللينكس"""
    if not text:
        return ""
    return arabic_reshaper.reshape(text)

def hash_password(password):
    """تشفير كلمة المرور بنظام SHA-256 لحمايتها داخل قاعدة البيانات"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_resource_path(relative_path):
    """جلب المسار الحقيقي للأيقونة لضمان ظهورها داخل التطبيق المستقل"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# =====================================================================
# 2. إدارة قاعدة البيانات المحلية (SQLite)
# =====================================================================
def init_db():
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

# =====================================================================
# 3. نافذة تسجيل الدخول وإنشاء الحساب (Login Window)
# =====================================================================
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(fix_arabic("تسجيل الدخول / حساب جديد"))
        self.setGeometry(150, 150, 400, 300)
        self.setStyleSheet("background-color: #F4F6F9;")
        self.setWindowIcon(QIcon(get_resource_path("logo.png"))) 
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel(fix_arabic("🎮 نظام دخول اللاعبين 🎮"), self)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #2C3E50; margin-bottom: 20px; qproperty-alignment: AlignCenter;")
        layout.addWidget(title)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText(fix_arabic("اسم المستخدم"))
        self.username_input.setFixedWidth(280)
        self.username_input.setFixedHeight(35)
        self.username_input.setStyleSheet("background-color: white; border: 1px solid #BDC3C7; border-radius: 5px; padding: 5px;")
        self.username_input.setLayoutDirection(Qt.RightToLeft)
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText(fix_arabic("كلمة المرور"))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(280)
        self.password_input.setFixedHeight(35)
        self.password_input.setStyleSheet("background-color: white; border: 1px solid #BDC3C7; border-radius: 5px; padding: 5px;")
        self.password_input.setLayoutDirection(Qt.RightToLeft)
        layout.addWidget(self.password_input)

        btn_layout = QHBoxLayout()
        
        login_btn = QPushButton(fix_arabic("تسجيل الدخول"), self)
        login_btn.setStyleSheet("background-color: #3498DB; color: white; border-radius: 5px; font-weight: bold; padding: 8px;")
        login_btn.clicked.connect(self.handle_login)
        btn_layout.addWidget(login_btn)

        reg_btn = QPushButton(fix_arabic("حساب جديد"), self)
        reg_btn.setStyleSheet("background-color: #2ECC71; color: white; border-radius: 5px; font-weight: bold; padding: 8px;")
        reg_btn.clicked.connect(self.handle_register)
        btn_layout.addWidget(reg_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, fix_arabic("خطأ"), fix_arabic("يرجى ملء جميع الحقول"))
            return

        conn = sqlite3.connect("quiz_game.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password, high_score FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close() # إغلاق فوري للاتصال بأمان

        if row and row[0] == hash_password(password):
            self.quiz_window = QuizPyQt5(username, row[1])
            self.quiz_window.show()
            self.close()
        else:
            QMessageBox.critical(self, fix_arabic("فشل الدخول"), fix_arabic("اسم المستخدم أو كلمة المرور خاطئة!"))

    def handle_register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, fix_arabic("خطأ"), fix_arabic("يرجى ملء جميع الحقول"))
            return

        hashed_pass = hash_password(password)

        conn = sqlite3.connect("quiz_game.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pass))
            conn.commit()
            QMessageBox.information(self, fix_arabic("نجاح"), fix_arabic("تم إنشاء الحساب بنجاح! يمكنك الدخول الآن."))
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, fix_arabic("خطأ"), fix_arabic("اسم المستخدم مسجل مسبقاً!"))
        finally:
            conn.close() # يضمن إغلاق قاعدة البيانات حتماً حتى لو حدث خطأ تكرار اسم مستخدم لمنع حدوث قفل للملف


# =====================================================================
# 4. نافذة اللعبة الأساسية (Main Quiz Window)
# =====================================================================
class QuizPyQt5(QWidget):
    def __init__(self, username, high_score):
        super().__init__()
        self.username = username
        self.high_score = high_score
        
        self.setWindowTitle(fix_arabic(f"تحدي بايثون - اللاعب: {self.username}"))
        self.setGeometry(100, 100, 550, 500)
        self.setStyleSheet("background-color: #F4F6F9;")
        self.setWindowIcon(QIcon(get_resource_path("logo.png")))

        # مستودع أسئلة ضخم يحتوي على 100 سؤال متساوي الصعوبة
        self.questions_pool = [
            {"question": "ما هي الدالة المستخدمة لطباعة النصوص في بايثون؟", "options": ["echo()", "print()", "output()", "log()"], "answer": "print()"},
            {"question": "أي من الخيارات التالية يُسخدم لتعريف دالة جديدة؟", "options": ["function", "def", "func", "define"], "answer": "def"},
            {"question": "ما هي نتيجة تنفيذ الأمر التالي: print(10 // 3) ؟", "options": ["3.333", "3", "1", "0"], "answer": "3"},
            {"question": "أي من هياكل البيانات التالية يتم تعريفه بالأقواس [ ] ؟", "options": ["List", "Dictionary", "Tuple", "Set"], "answer": "List"},
            {"question": "ما هي الدالة المستخدمة لإضافة عنصر في نهاية القائمة (List)؟", "options": ["add()", "insert()", "append()", "extend()"], "answer": "append()"},
            {"question": "أي مما يلي ليس اسماً صحيحاً لمتغير في بايثون؟", "options": ["my_var", "var_1", "1_var", "_var"], "answer": "1_var"},
            {"question": "كيف نكتب تعليقاً (Comment) من سطر واحد في بايثون؟", "options": ["// تعليق", "# تعليق", "/* تعليق */", "<!-- تعليق -->"], "answer": "# تعليق"},
            {"question": "ما هي الكلمة المفتاحية المستخدمة لإيقاف حلقة التكرار (Loop) فوراً؟", "options": ["stop", "break", "exit", "continue"], "answer": "break"},
            {"question": "ما هو نوع البيانات الناتج عن الأمر التالي: x = 5.5 ؟", "options": ["int", "string", "float", "boolean"], "answer": "float"},
            {"question": "ما هي الدالة التي تعيد طول القائمة أو عدد عناصرها؟", "options": ["length()", "size()", "count()", "len()"], "answer": "len()"},
            {"question": "أي من الرموز التالية يمثل عملية باقي القسمة (Modulus) في بايثون؟", "options": ["/", "//", "%", "^"], "answer": "%"},
            {"question": "كيف نقوم بتحويل نص الرقم '10' إلى رقم صحيح؟", "options": ["int('10')", "str('10')", "float('10')", "convert('10')"], "answer": "int('10')"},
            {"question": "ما هي الكلمة المفتاحية المستخدمة للتحقق من شرط إضافي بعد الشرط الأول؟", "options": ["else if", "elseif", "elif", "if else"], "answer": "elif"},
            {"question": "أي من هياكل البيانات التالية لا يسمح بتكرار العناصر داخله؟", "options": ["List", "Tuple", "Set", "Array"], "answer": "Set"},
            {"question": "ما هي النتيجة البرمجية للأمر التالي: print('A' + 'B') ؟", "options": ["AB", "A B", "Error", "None"], "answer": "AB"},
            {"question": "أي دالة تستخدم لحذف عنصر معين من قائمة بناءً على قيمته؟", "options": ["delete()", "remove()", "discard()", "pop()"], "answer": "remove()"},
            {"question": "ما هي النتيجة البرمجية لتنفيذ الكود: print(type([])) ？", "options": ["<class 'list'>", "<class 'dict'>", "<class 'tuple'>", "<class 'set'>"], "answer": "<class 'list'>"},
            {"question": "كيف يتم بدء حلقة تكرار تمر 5 مرات من الرقم 0 إلى 4؟", "options": ["for i in range(5)", "for i in range(1, 5)", "while i < 4", "loop 5 times"], "answer": "for i in range(5)"},
            {"question": "أي مما يلي يُسخدم لفتح ملف خارجي في بايثون؟", "options": ["open()", "read()", "file()", "load()"], "answer": "open()"},
            {"question": "ما هي الكلمة المفتاحية المستخدمة لتمرير دالة فارغة بدون كتابة كود داخلها؟", "options": ["null", "void", "pass", "skip"], "answer": "pass"},
            {"question": "ما هي نتيجة تنفيذ الأمر: print(3 * 'A') ؟", "options": ["AAA", "3A", "Error", "A3"], "answer": "AAA"},
            {"question": "أي من الخيارات التالية يُعرف كقاموس (Dictionary) فارغ؟", "options": ["[]", "()", "{}", "set()"], "answer": "{}"},
            {"question": "ما هي دالة الإدخال البرمجية لاستقبال البيانات من المستخدم؟", "options": ["get()", "read()", "input()", "scan()"], "answer": "input()"},
            {"question": "أي كلمة مفتاحية تستخدم لإعادة قيمة من داخل دالة؟", "options": ["give", "send", "return", "output"], "answer": "return"},
            {"question": "ما هي القيمة البولينية الافتراضية للنص الفارغ '' عند تحويله عبر bool() ؟", "options": ["True", "False", "None", "Error"], "answer": "False"},
            {"question": "أي دالة تستخدم لترتيب عناصر القائمة ترتيباً تصاعدياً؟", "options": ["sort()", "order()", "arrange()", "reverse()"], "answer": "sort()"},
            {"question": "ما هو الامتداد الرسمي المعتمد لملفات كود بايثون؟", "options": [".pt", ".py", ".pyt", ".class"], "answer": ".py"},
            {"question": "أي مما يلي يمثل القيمة غير المعرفة أو الفارغة في بايثون؟", "options": ["Null", "NaN", "None", "Void"], "answer": "None"},
            {"question": "ما هي النتيجة البرمجية للأمر: print(bool(0)) ؟", "options": ["True", "False", "None", "Error"], "answer": "False"},
            {"question": "أي دالة مدمجة تستخدم لإنشاء أرقام عشوائية صحيحة؟", "options": ["random.rand()", "random.randint()", "random.integer()", "random.choice()"], "answer": "random.randint()"},
            {"question": "ما هو هيكل البيانات الذي يربط المفاتيح (Keys) بالقيم (Values)؟", "options": ["List", "Tuple", "Set", "Dictionary"], "answer": "Dictionary"},
            {"question": "كيف نتحقق برمجياً أن المتغير x يساوي 10؟", "options": ["x = 10", "x == 10", "x === 10", "x is 10"], "answer": "x == 10"},
            {"question": "أي دالة تستخدم لتحويل رقم إلى نص (String)؟", "options": ["str()", "text()", "string()", "to_str()"], "answer": "str()"},
            {"question": "ما هي نتيجة الكود التالي: print(5 % 2) ؟", "options": ["2.5", "2", "1", "0"], "answer": "1"},
            {"question": "أي مما يلي يُستخدم لالتقاط الاستثناءات (Exceptions) والأخطاء؟", "options": ["try/except", "catch/throw", "if/error", "error/handle"], "answer": "try/except"},
            {"question": "ما هي النتيجة البرمجية للكود: print('abc'.upper()) ؟", "options": ["Abc", "abc", "ABC", "Error"], "answer": "ABC"},
            {"question": "أي دالة مدمجة تستخدم لحساب مجموع عناصر قائمة رقمية؟", "options": ["total()", "sum()", "add()", "count()"], "answer": "sum()"},
            {"question": "ما هو الكائن الأساسي المستخدم في بايثون للتعامل مع الوقت؟", "options": ["time", "clock", "datetime", "date"], "answer": "time"},
            {"question": "كيف يتم حذف مساحة الفراغات الزائدة من بداية ونهاية النص؟", "options": ["strip()", "trim()", "clean()", "cut()"], "answer": "strip()"},
            {"question": "ماذا تعيد دالة ()keys الخاصة بالقواميس؟", "options": ["جميع القيم", "جميع المفاتيح", "القاموس بالكامل", "حجم القاموس"], "answer": "جميع المفاتيح"},
            {"question": "أي دالة تستخدم لإيجاد القيمة الصغرى في مجموعة أرقام؟", "options": ["min()", "max()", "lowest()", "small()"], "answer": "min()"},
            {"question": "ما هي نتيجة تنفيذ الكود: print(10 / 2) ؟", "options": ["5", "5.0", "2", "2.0"], "answer": "5.0"},
            {"question": "أي مما يلي يمثل بيئة عمل (Framework) لبناء المواقع باستخدام بايثون؟", "options": ["Django", "React", "Laravel", "Spring"], "answer": "Django"},
            {"question": "كيف نقوم باستيراد مكتبة خارجية في بايثون؟", "options": ["include", "import", "require", "load"], "answer": "import"},
            {"question": "ما هي الكلمة المستخدمة لتعريف فئة برمجية (Class) جديدة؟", "options": ["object", "def", "class", "struct"], "answer": "class"},
            {"question": "ما هو هيكل البيانات غير القابل للتعديل (Immutable) بعد إنشائه؟", "options": ["List", "Tuple", "Dictionary", "Set"], "answer": "Tuple"},
            {"question": "أي من الخيارات التالية يُستدعى تلقائياً عند بناء كائن جديد من كلاس؟", "options": ["main", "init", "start", "construct"], "answer": "init"},
            {"question": "ما هي نتيجة الكود: print('Python'[0]) ؟", "options": ["P", "y", "n", "Error"], "answer": "P"},
            {"question": "أي دالة تُستخدم لعرض النتيجة الأخيرة في نافذة الأوامر بترميز معين؟", "options": ["encode()", "decode()", "print()", "format()"], "answer": "print()"},
            {"question": "ما هي نتيجة الكود التالي: print('a' in 'apple') ؟", "options": ["True", "False", "None", "Error"], "answer": "True"},
            {"question": "أي رمز يستخدم لضرب الأرقام في لغة بايثون؟", "options": ["x", "X", "", "^"], "answer": ""},
            {"question": "ما هي دالة القواميس التي تعيد القيمة وتحذف المفتاح في آن واحد؟", "options": ["pop()", "remove()", "delete()", "clear()"], "answer": "pop()"},
            {"question": "أي دالة مدمجة تستخدم لحساب القيمة المطلقة (Absolute) للرقم؟", "options": ["abs()", "absolute()", "math.abs()", "num()"], "answer": "abs()"},
            {"question": "ما هي النتيجة البرمجية للكود: print('1' + '1') ؟", "options": ["2", "11", "Error", "None"], "answer": "11"},
            {"question": "كيف يتم فصل نص طويل إلى قائمة كلمات بناءً على الفراغات؟", "options": ["split()", "divide()", "cut()", "separate()"], "answer": "split()"},
            {"question": "ما هي النتيجة البرمجية للكود: print(not True) ؟", "options": ["True", "False", "None", "Error"], "answer": "False"},
            {"question": "أي مكتبة تستخدم بشكل رسمي مدمج لحساب العمليات الرياضية المتقدمة؟", "options": ["math", "calc", "mathematics", "science"], "answer": "math"},
            {"question": "ماذا تعني العلامة البرمجية =+ في الكود x += 1 ؟", "options": ["x يساوي 1", "إضافة 1 لقيمة x الحالية", "ضرب x في 1", "مقارنة x بـ 1"], "answer": "إضافة 1 لقيمة x الحالية"},
            {"question": "أي مما يلي يُعد محرر أكواد مخصص شهير للغة بايثون؟", "options": ["PyCharm", "Photoshop", "Excel", "Word"], "answer": "PyCharm"},
            {"question": "ما هي النتيجة البرمجية للكود: print(10 - 2 * 3) ؟", "options": ["24", "4", "8", "14"], "answer": "4"},
            {"question": "أي دالة برمجية تفتح علبة حوار منبثقة بسيطة في PyQt5؟", "options": ["QMessageBox", "QDialog", "QWindow", "QPopup"], "answer": "QMessageBox"},
            {"question": "ما هي دالة القوائم التي تفرغ القائمة تماماً من كافة العناصر؟", "options": ["clear()", "empty()", "remove_all()", "delete()"], "answer": "clear()"},
            {"question": "أي مما يلي يستخدم لجمع كلمتين نصيتين في متغير واحد؟", "options": ["دمج النصوص (Concatenation)", "الضرب", "القسمة الصحيحة", "المجموعات"], "answer": "دمج النصوص (Concatenation)"},
            {"question": "كيف نتحقق برمجياً أن المتغير x لا يساوي 5؟", "options": ["x != 5", "x <> 5", "x not 5", "x == ! 5"], "answer": "x != 5"},
            {"question": "ما هو نوع البيانات الذي يمثله الرقم 100 في بايثون؟", "options": ["float", "int", "string", "boolean"], "answer": "int"},
            {"question": "ماذا يحدث عند تنفيذ الأمر التالي: print('Python'[-1]) ؟", "options": ["P", "n", "Error", "o"], "answer": "n"},
            {"question": "أي دالة تستخدم لتغيير حالة الحروف الإنجليزية إلى صغيرة كلها؟", "options": ["lower()", "small()", "upper()", "capitalize()"], "answer": "lower()"},
            {"question": "ما هي نتيجة الكود التالي: print(type(True)) ؟", "options": ["<class 'bool'>", "<class 'int'>", "<class 'str'>", "<class 'None'>"], "answer": "<class 'bool'>"},
            {"question": "أي من الكلمات التالية تستخدم لتعريف متغير كوني عام داخل الدالة؟", "options": ["global", "public", "universal", "outer"], "answer": "global"},
            {"question": "ماذا تفعل دالة count() عند تطبيقها على النص؟", "options": ["تحسب طول النص", "تحسب عدد مرات تكرار حرف أو نص معين", "تحسب عدد الكلمات", "تحذف الأرقام"], "answer": "تحسب عدد مرات تكرار حرف أو نص معين"},
            {"question": "أي دالة مدمجة تستخدم لعرض جولة تفاعلية من أرقام المعرفات والعناصر؟", "options": ["enumerate()", "list()", "range()", "index()"], "answer": "enumerate()"},
            {"question": "ما هي نتيجة تنفيذ الكود: print(2 ** 4) ؟", "options": ["8", "16", "64", "32"], "answer": "16"},
            {"question": "كيف نكتب الجملة الشرطية العادية التي تنفذ كوداً إذا كان x أكبر من 5؟", "options": ["if x > 5:", "if (x > 5)", "if x > 5 then", "check x > 5"], "answer": "if x > 5:"},
            {"question": "أي دالة تستخدم لاستبدال كلمة بكلمة أخرى داخل النص؟", "options": ["replace()", "change()", "switch()", "update()"], "answer": "replace()"},
            {"question": "ما هو الكائن الذي يمثل نافذة فارغة أساسية في مكتبة PyQt5؟", "options": ["QWidget", "QLabel", "QPushButton", "QMainWindow"], "answer": "QWidget"},
            {"question": "ما هي نتيجة الكود التالي: print(5 == 5.0) ؟", "options": ["True", "False", "None", "Error"], "answer": "True"},
            {"question": "أي مما يلي يمثل صيغة لرفع المشروعات البرمجية ومشاركتها مع العالم؟", "options": ["GitHub", "Google", "Facebook", "YouTube"], "answer": "GitHub"},
            {"question": "ما هي دالة القوائم التي تعيد عكس ترتيب عناصر القائمة بالكامل؟", "options": ["reverse()", "flip()", "invert()", "sort(reverse=True)"], "answer": "reverse()"},
            {"question": "أي كلمة مفتاحية تُستدعى لتنفيذ كود نهائي حتمي سواء حدث خطأ أم لا؟", "options": ["finally", "always", "end", "except"], "answer": "finally"},
            {"question": "ما هي النتيجة البرمجية للكود: print('10' * 2) ؟", "options": ["20", "1010", "Error", "102"], "answer": "1010"},
            {"question": "أي دالة تستخدم لمعرفة كافة الصلاحيات والدوال التابعة لكائن معين؟", "options": ["dir()", "help()", "type()", "list()"], "answer": "dir()"},
            {"question": "ما هي الكلمة المفتاحية المستخدمة للانتقال للدورة التالية في الـ Loop وتجاهل الكود الحالي؟", "options": ["continue", "skip", "pass", "next"], "answer": "continue"},
            {"question": "أي مما يلي يمثل مكتبة مدمجة لإنشاء واجهات نصية تفاعلية سريعة؟", "options": ["sys", "os", "math", "time"], "answer": "sys"},
            {"question": "ما هي القيمة الافتراضية لعنصر القائمة الأخير عند حذفه بـ pop() بدون تحديد معامل؟", "options": ["العنصر الأول", "العنصر الأخير", "حذف كل القائمة", "يسبب خطأ برمجياً"], "answer": "العنصر الأخير"},
            {"question": "ماذا تعني التهيئة الذكية المكتوبة بصيغة list comprehension؟", "options": ["إنشاء قائمة مختصرة بسطر كود واحد", "ضغط ملفات الكود", "حفظ البيانات في SQL", "تشفير كلمات المرور"], "answer": "إنشاء قائمة مختصرة بسطر كود واحد"},
            {"question": "أي مما يلي يُعد الطريقة القياسية لقراءة سطر كامل من ملف نصي مفتوح؟", "options": ["readline()", "read()", "get_line()", "scan()"], "answer": "readline()"},
            {"question": "ما هي نتيجة الكود التالي: print(float(5)) ؟", "options": ["5", "5.0", "0.5", "Error"], "answer": "5.0"},
            {"question": "أي رمز يستخدم لتمثيل عملية الأس أو القوة الرياضية في بايثون؟", "options": ["^", "", "*", "pow"], "answer": ""},
            {"question": "كيف نتحقق برمجياً من نوع كائن المتغير x؟", "options": ["type(x)", "kind(x)", "class(x)", "check(x)"], "answer": "type(x)"},
            {"question": "ما هو الاختصار المكتوب برمجياً لتنفيذ حلقة تكرار تعتمد على شرط دائم التحقق؟", "options": ["while True:", "for True:", "loop always:", "do while:"], "answer": "while True:"},
            {"question": "أي دالة مدمجة تستخدم لدمج عناصر قائمة نصية لتصبح نصاً واحداً يفصل بينها رمز معين؟", "options": ["join()", "merge()", "concat()", "connect()"], "answer": "join()"},
            {"question": "ما هي نتيجة تنفيذ الأمر: print('Hello'.find('e')) ؟", "options": ["0", "1", "2", "-1"], "answer": "1"},
            {"question": "أي مما يلي يمثل كلمة مفتاحية لحذف متغير أو عنصر بالكامل من الذاكرة؟", "options": ["del", "remove", "clear", "discard"], "answer": "del"},
            {"question": "ماذا يحدث عند محاولة الوصول لمفتاح غير موجود في القاموس عبر dict['key'] ؟", "options": ["يعيد None", "يحدث خطأ KeyError", "ينشئ المفتاح تلقائياً", "يعيد نصاً فارغاً"], "answer": "يحدث خطأ KeyError"},
            {"question": "أي دالة قواميس آمنة تعيد قيمة افتراضية إذا لم يكن المفتاح موجوداً وتمنع انهيار التطبيق؟", "options": ["get()", "find()", "fetch()", "pop()"], "answer": "get()"},
            {"question": "ما هي نتيجة الكود التالي: print(len('Py')) ؟", "options": ["1", "2", "3", "Error"], "answer": "2"},
            {"question": "أي مما يلي يمثل الأسلوب الاحترافي لعزل حزم مشروع بايثون عن ملفات النظام؟", "options": ["البيئة الوهمية (Virtual Environment)", "ملفات الـ EXE", "قواعد بيانات SQL", "الواجهات الرسومية"], "answer": "البيئة الوهمية (Virtual Environment)"},
            {"question": "ما هي نتيجة تنفيذ الأمر: print(abs(-10)) ؟", "options": ["-10", "10", "0", "Error"], "answer": "10"},
            {"question": "أي دالة تستخدم في بايثون للتحقق مما إذا كان النص ينتهي بحرف أو كلمة معينة؟", "options": ["endswith()", "finishwith()", "last()", "check_end()"], "answer": "endswith()"},
            {"question": "ما هي النتيجة البرمجية للأمر التالي: print(bool([])) ؟", "options": ["True", "False", "None", "Error"], "answer": "False"}]
                # التعديل: اختيار 10 أسئلة عشوائية تماماً في كل جولة لعب من أصل الـ 100
        # (هذا الجزء يوضع في نهاية دالة __init__ الخاصة بكلاس QuizPyQt5)
        self.quiz_data = random.sample(self.questions_pool, 10)
        self.current_index = 0
        self.score = 0
        self.time_left = 10
        self.points_per_question = 10

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)

        self.info_label = QLabel(fix_arabic(f"اللاعب: {self.username}  |  🏆 أعلى سكور سابق: {self.high_score}"), self)
        self.info_label.setFont(QFont("Arial", 11))
        self.info_label.setStyleSheet("color: #7F8C8D; qproperty-alignment: AlignCenter;")
        self.main_layout.addWidget(self.info_label)

        self.score_label = QLabel(fix_arabic(f"النقاط الحالية: {self.score}"), self)
        self.score_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.score_label.setStyleSheet("color: #2C3E50; qproperty-alignment: AlignCenter;")
        self.main_layout.addWidget(self.score_label)

        self.timer_label = QLabel(fix_arabic(f"⏱️ الوقت المتبقي: {self.time_left}"), self)
        self.timer_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.timer_label.setStyleSheet("color: #E74C3C; qproperty-alignment: AlignCenter;")
        self.main_layout.addWidget(self.timer_label)

        self.question_label = QLabel("", self)
        self.question_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("color: #34495E; margin: 20px; qproperty-alignment: AlignCenter;")
        self.main_layout.addWidget(self.question_label)

        self.buttons = []
        for i in range(4):
            btn = QPushButton("", self)
            btn.setFont(QFont("Arial", 12))
            btn.setFixedWidth(400)
            btn.setFixedHeight(45)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("QPushButton { background-color: white; border: 2px solid #BDC3C7; border-radius: 8px; color: #2C3E50; } QPushButton:hover { background-color: #3498DB; color: white; }")
            btn.clicked.connect(lambda checked, idx=i: self.check_answer(idx))
            self.main_layout.addWidget(btn)
            self.buttons.append(btn)

        self.setLayout(self.main_layout)
        self.display_question()

    def display_question(self):
        if self.current_index < len(self.quiz_data):
            q = self.quiz_data[self.current_index]
            self.question_label.setText(fix_arabic(f"السؤال {self.current_index + 1}: {q['question']}"))
            
            for i, option in enumerate(q['options']):
                self.buttons[i].setText(fix_arabic(option))
                self.buttons[i].setEnabled(True)
                self.buttons[i].setStyleSheet("QPushButton { background-color: white; border: 2px solid #BDC3C7; border-radius: 8px; color: #2C3E50; } QPushButton:hover { background-color: #3498DB; color: white; }")
            
            self.time_left = 10
            self.timer_label.setText(fix_arabic(f"⏱️ الوقت المتبقي: {self.time_left}"))
            self.timer.start(1000)
        else:
            self.end_quiz()

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(fix_arabic(f"⏱️ الوقت المتبقي: {self.time_left}"))
        if self.time_left == 0:
            self.timer.stop()
            self.handle_timeout()

    def handle_timeout(self):
        for btn in self.buttons:
            btn.setEnabled(False)
        q = self.quiz_data[self.current_index]
        
        msg = QMessageBox(self)
        msg.setWindowTitle(fix_arabic("انتهى الوقت!"))
        msg.setText(fix_arabic(f"⏱️ للأسف انتهى وقتك.\nالإجابة الصحيحة هي: {q['answer']}"))
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()
        
        self.current_index += 1
        self.display_question()

    def check_answer(self, selected_idx):
        self.timer.stop()
        q = self.quiz_data[self.current_index]
        selected_option = q['options'][selected_idx]
        msg = QMessageBox(self)
        
        if selected_option == q['answer']:
            self.score += self.points_per_question
            self.score_label.setText(fix_arabic(f"النقاط الحالية: {self.score}"))
            self.buttons[selected_idx].setStyleSheet("background-color: #2ECC71; color: white; border-radius: 8px;")
            msg.setWindowTitle(fix_arabic("أحسنت!"))
            msg.setText(fix_arabic(f"✨ إجابة صحيحة! كسبت {self.points_per_question} نقطة."))
            msg.setIcon(QMessageBox.Information)
        else:
            self.buttons[selected_idx].setStyleSheet("background-color: #E74C3C; color: white; border-radius: 8px;")
            msg.setWindowTitle(fix_arabic("للأسف!"))
            msg.setText(fix_arabic(f"❌ إجابة خاطئة.\nالإجابة الصحيحة هي: {q['answer']}"))
            msg.setIcon(QMessageBox.Critical)
            
        msg.exec_()
        self.current_index += 1
        self.display_question()

    def end_quiz(self):
        max_possible = len(self.quiz_data) * self.points_per_question
        
        if self.score > self.high_score:
            self.high_score = self.score
            conn = sqlite3.connect("quiz_game.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET high_score = ? WHERE username = ?", (self.score, self.username))
            conn.commit()
            conn.close()
            announcement = f"🏆 رقم قياسي جديد مذهل! لقد سجلت {self.score} نقطة!"
        else:
            announcement = f"🏁 جولة رائعة! مجموع نقاطك اليوم: {self.score} من أصل {max_possible}"

        self.timer_label.hide()
        self.question_label.hide()
        for btn in self.buttons:
            btn.hide()

        self.info_label.setText(fix_arabic(f"اللاعب: {self.username}  |  🏆 أعلى رقم قياسي دائم: {self.high_score}"))
        self.score_label.setText(fix_arabic(announcement))
        
        self.end_buttons_layout = QHBoxLayout()
        
        self.restart_btn = QPushButton(fix_arabic("🔄 إعادة اللعب"), self)
        self.restart_btn.setFixedWidth(180)
        self.restart_btn.setFixedHeight(45)
        self.restart_btn.setStyleSheet("background-color: #2ECC71; color: white; font-weight: bold; border-radius: 5px;")
        self.restart_btn.clicked.connect(self.restart_game)
        self.end_buttons_layout.addWidget(self.restart_btn)

        self.exit_btn = QPushButton(fix_arabic("🚪 خروج"), self)
        self.exit_btn.setFixedWidth(180)
        self.exit_btn.setFixedHeight(45)
        self.exit_btn.setStyleSheet("background-color: #E74C3C; color: white; font-weight: bold; border-radius: 5px;")
        self.exit_btn.clicked.connect(self.close)
        self.end_buttons_layout.addWidget(self.exit_btn)

        self.main_layout.addLayout(self.end_buttons_layout)

    def restart_game(self):
        self.restart_btn.deleteLater()
        self.exit_btn.deleteLater()
        
        self.current_index = 0
        self.score = 0
        # اختيار 10 أسئلة عشوائية جديدة عند إعادة اللعب لمنع التكرار
        self.quiz_data = random.sample(self.questions_pool, 10)
        
        self.score_label.setText(fix_arabic(f"النقاط الحالية: {self.score}"))
        self.timer_label.show()
        self.question_label.show()
        for btn in self.buttons:
            btn.show()
            
        self.display_question()

# =====================================================================
# 5. محرك تشغيل النظام الرئيسي
# =====================================================================
if __name__ == "__main__":
    init_db()  # تهيئة قاعدة البيانات تلقائياً
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())

