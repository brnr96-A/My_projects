# 🧮 مسار إتقان مكتبة pandas من الصفر | pandas Lib

###  إعداد البيئة البرمجية وتثبيت المكتبة
```bash
# إنشاء بيئة افتراضية (ينصح به لعزل المشروع)
python -m ML_env venv

# تفعيل البيئة الافتراضية

# على نظام Linux:
source ML_env/bin/activate

# تثبيت مكتبة NumPy
pip install pandas
```
📂 هيكل المجلدات والملفات لـ Pandas (Repository Structure)

📸 ML-Roadmap-Pandas/
│
├── 📂 Pandas_Guide/
│   ├── 📄 README.md     # الشرح النظري لـ Pandas (الهياكل الداخلية والفرق عن NumPy)
│   ├── 📓 01_series_and_dataframes.ipynb # كود: السلاسل، الجداول، القراءة والكتابة (CSV, Excel)
│   ├── 📓 02_data_cleaning.ipynb     # كود: تنظيف البيانات، معالجة القيم المفقودة والمكررة
│   ├── 📓 03_filtering_and_sorting.ipynb # كود: تصفية البيانات المتقدمة، الترتيب، والـ Slicing
│   ├── 📓 04_grouping_and_aggregation.ipynb # كود: تجميع البيانات (GroupBy) والدمج (Merge/Join)
│   └── 📓 05_real_world_preprocessing.ipynb # تمرين تطبيقي: تجهيز مجموعة بيانات حقيقية للـ ML
    ├── 📓 06_advanced_transformations.ipynb  # إضافات: دوال التحويل المتقدمة والتحكم بالأوقات
│   └── 📓 07_handling_large_data.ipynb       # إضافات: التعامل مع البيانات الضخمة وكفاءة الذاكرة


1. **Pandas Series (أحادية البعد):** مصفوفة تشبه متجه NumPy ولكنها تمتلك كشافات مخصصة (Labeled Index). يمكن أن تكون الفهارس نصوصاً بدلاً من أرقام.
2. **Pandas DataFrame (ثنائية البعد):** البنية الأهم، وهي جدول بيانات متكامل يشبه جداول SQL أو Excel. يتكون من عدة أسطر (Samples) وأعمدة (Features)، وكل عمود عبارة عن `Series` مستقلة بنوع بيانات خاص بها.

## 📚 (جدول المحتويات)
* إنشاء السلاسل والجداول الإحصائية واستكشاف البيانات (`head`, `info`, `describe`).
* تكتيكات تنظيف البيانات من القيم المفقودة والمكررة وتجهيزها لـ NumPy.
* التصفية المتقدمة واستخراج الميزات باستخدام شروط `loc` و `iloc`.
* **[جديد]** هندسة الميزات المتقدمة وتطويع التواريخ والسلاسل الزمنية عبر `apply` و `transform`.
* **[جديد]** تكتيكات الـ Memory Optimization ومعالجة الملفات العملاقة عبر الـ Chunking لتفادي انهيار الذاكرة.