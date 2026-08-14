import sys
import random
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

# قوائم الإجابات للكرة السحرية
positive_res = ["نعم، بكل تأكيد!", "يبدو الأمر مبشراً جداً.", "الإشارات كلها تقول نعم."]
neutral_res = ["يرجى إعادة المحاولة لاحقاً.", "الرؤية غير واضحة حالياً."]
negative_res = ["لا تعتمد على ذلك.", "مصادرنا القوية تقول لا."]
all_responses = positive_res + neutral_res + negative_res

math_symbols = ['=', '+', '-', '*', '/', '%', '^', '<', '>', '(', ')', '√']

# تصنيف أدوات الاستفهام
yes_no_keywords = ["هل", "أ", "is", "can", "will", "do", "does", "should", "would"]
open_ended_keywords = [
    "كيف", "لماذا", "متى", "أين", "من", "ماذا", "كم", "ما", "أيها",
    "how", "why", "when", "where", "who", "what", "which"
]

last_question = ""
last_answer = ""
questions_history = []
user_name = "صديقي"

def analyze_question_type(text):
    text_lower = text.strip().lower()
    words = text_lower.split()
    
    if not words:
        return "not_a_question"
        
    for word in words:
        cleaned_word = word.strip("؟?") 
        if cleaned_word in open_ended_keywords:
            return "open_ended"

    first_word = words[0]
    
    if first_word in yes_no_keywords:
        return "valid_yes_no"
        
    if first_word.startswith("أ") and len(first_word) > 2:
        valid_arabic_int = ["أأصنع", "أأسافر", "أأذهب", "أهي", "أهو", "أأنت", "أأنتم", "أخالد", "أسعيد"]
        if first_word in valid_arabic_int or first_word.startswith("أأ"):
            return "valid_yes_no"

    informational_starters = [
        "أريد", "أصنع", "أذهب", "أنا", "أستطيع", "هو", "هي", "نحن", "هم", "أنت", 
        "الجو", "اليوم", "الكتاب", "السيارة", "أحمد", "محمد"
    ]

    if text_lower.endswith("؟") or text_lower.endswith("?"):
        if first_word in informational_starters:
            return "just_talk"
        return "valid_yes_no"
        
    return "just_talk"

# --- الدوال البرمجية ---

def save_name():
    global user_name
    name_input = entry_name.text().strip()
    if name_input:
        user_name = name_input
    
    lbl_welcome.setText(f"أهلاً بك يا {user_name}! أنا جاهزة لمساعدتك.")
    widget_name.hide()
    widget_quiz.show()

def process_question():
    global last_question, last_answer, questions_history
    
    user_input = entry_question.text().strip()
    
    if user_input == "":
        QMessageBox.warning(window, "تنبيه", "⚠️ لا يمكنك ترك خانة السؤال فارغة!")
        return

    normalized_input = user_input.replace(" و ", ",")
    questions_list = normalized_input.split(",")
    cleaned_questions = [q.strip() for q in questions_list if q.strip() != ""]

    if len(cleaned_questions) > 2:
        QMessageBox.critical(window, "خطأ", "⚠️ يرجى طرح سؤالين كحد أقصى في المرة الواحدة!")
        return

    for q in cleaned_questions:
        if any(sym in q for sym in math_symbols):
            QMessageBox.critical(window, "خطأ في الإدخال", f"⚠️ خطأ في '{q}':\nيرجى كتابة سؤال وليس معادلة رياضية!")
            return
        elif q.isdigit():
            QMessageBox.critical(window, "خطأ في الإدخال", f"⚠️ خطأ في '{q}':\nلقد أدخلت رقماً صافياً!")
            return
            
        question_status = analyze_question_type(q)
        
        if question_status == "open_ended":
            QMessageBox.warning(
                window, 
                "سؤال خارج حدود المنطق", 
                f"⚠️ الجملة: '{q}'\nهو سؤال مفتوح يتطلب تفاصيل وشرحاً يفوق حدود (نعم أو لا)!\nيرجى إعادة صياغته ليبدأ بـ (هل...) لكي أتمكن من الإجابة."
            )
            return
        elif question_status == "just_talk":
            QMessageBox.warning(
                window, 
                "صياغة خاطئة", 
                f"⚠️ الجملة: '{q}' تبدو مجرد كلام عادي أو فضفضة!\nيرجى صياغة سؤال واضح ومحدد يحتمل الإجابة بنعم أو لا."
            )
            return

    final_output = ""

    for index, q in enumerate(cleaned_questions, 1):
        if q == last_question:
            final_output += f"💡 سؤال مكرر: {q}\n"
            final_output += f"🎱 الكرة تكرر: {last_answer}\n"
            final_output += "-----------------------\n"
            continue 

        while True:
            chosen_answer = random.choices(all_responses, weights=[0.20]*7)
            if chosen_answer != last_answer:
                break

        if len(cleaned_questions) > 1:
            final_output += f"❓ السؤال {index}: {q}\n"
        else:
            final_output += f"❓ سؤالك هو: {q}\n"
        
        final_output += f"🎱 الكرة تقول: {chosen_answer}\n"
        final_output += "-----------------------\n"

        last_question = q
        last_answer = chosen_answer
        questions_history.append(q)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("magic_8ball_history.txt", "a", encoding="utf-8") as file:
            file.write(f"[{current_time}] الاسم: {user_name} | السؤال: {q} | الإجابة: {chosen_answer}\n")

    lbl_result.setText(final_output)

def show_history():
    if not questions_history:
        QMessageBox.information(window, "سجل الأسئلة", "📜 السجل فارغ تماماً في هذه الجلسة.")
    else:
        history_text = "\n".join(f"{idx}. {q}" for idx, q in enumerate(questions_history, 1))
        QMessageBox.information(window, "سجل أسئلتك الحالية", history_text)

def clear_all():
    entry_question.clear()
    lbl_result.setText("🎱 بانتظار سؤالك...")


# --- تشغيل واجهة PyQt5 ---
app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("🔮 نظام الكرة السحرية الاحترافي المطوّر 🔮")
window.resize(500, 480)
window.setLayoutDirection(Qt.RightToLeft)

layout_main = QVBoxLayout()

lbl_main_title = QLabel("مستشار القرارات الذكي - المطور")
lbl_main_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1A237E;")
layout_main.addWidget(lbl_main_title)

lbl_welcome = QLabel("مرحباً بك! يرجى إدخال اسمك أولاً لتبدأ تجربة مخصصة.")
layout_main.addWidget(lbl_welcome)

# --- إطار إدخال الاسم ---
widget_name = QWidget()
layout_name = QHBoxLayout()
entry_name = QLineEdit()
entry_name.setPlaceholderText("اكتب اسمك هنا...")

# 🌟 ميزة جديدة: تفعيل Enter لحفظ الاسم
entry_name.returnPressed.connect(save_name)

btn_save_name = QPushButton("حفظ الاسم")
btn_save_name.clicked.connect(save_name)

layout_name.addWidget(entry_name)
layout_name.addWidget(btn_save_name)
widget_name.setLayout(layout_name)
layout_main.addWidget(widget_name)

# --- إطار الأسئلة والتحكم ---
widget_quiz = QWidget()
layout_quiz = QVBoxLayout()

lbl_prompt = QLabel("اكتب سؤالك أو سؤالين معاً (بفصلهما بحرف و أو فاصلة):")
layout_quiz.addWidget(lbl_prompt)

entry_question = QLineEdit()
entry_question.setPlaceholderText("هل سأنجح في الامتحان؟")

# تفعيل Enter لطرح السؤال
entry_question.returnPressed.connect(process_question)
layout_quiz.addWidget(entry_question)

widget_buttons = QWidget()
layout_buttons = QHBoxLayout()

btn_ask = QPushButton("🔮 اسأل الكرة السحرية")
btn_ask.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
btn_ask.clicked.connect(process_question)

btn_history = QPushButton("📜 عرض السجل")
btn_history.setStyleSheet("background-color: #FF9800; color: white;")
btn_history.clicked.connect(show_history)

btn_clear = QPushButton("مسح")
btn_clear.setStyleSheet("background-color: #9E9E9E; color: white;")
btn_clear.clicked.connect(clear_all)

layout_buttons.addWidget(btn_ask)
layout_buttons.addWidget(btn_history)
layout_buttons.addWidget(btn_clear)
widget_buttons.setLayout(layout_buttons)
layout_quiz.addWidget(widget_buttons)

lbl_result = QLabel("🎱 بانتظار سؤالك...")
lbl_result.setStyleSheet("font-size: 13px; font-weight: bold; color: #2E7D32;")
layout_quiz.addWidget(lbl_result)

widget_quiz.setLayout(layout_quiz)
widget_quiz.hide()
layout_main.addWidget(widget_quiz)

# --- 🌟 ميزة جديدة: إضافة زر الخروج الأنيق في الأسفل ---
btn_exit = QPushButton("❌ خروج من البرنامج")
btn_exit.setStyleSheet("background-color: #D32F2F; color: white; font-weight: bold; margin-top: 10px;")
btn_exit.clicked.connect(window.close) # ربط الزر بحدث إغلاق النافذة آلياً
layout_main.addWidget(btn_exit)

window.setLayout(layout_main)
window.show()

sys.exit(app.exec_())
