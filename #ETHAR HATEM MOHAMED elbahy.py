import tkinter as tk
from tkinter import ttk, messagebox

# --- وظائف الواجهة الخلفية (Backend) التمثيلية ---
total_balance = 5000.00
expense_list = []

def add_expense():
    """وظيفة إضافة النفقات وحساب الرصيد الجديد."""
    global total_balance
    try:
        # الحصول على المدخلات من حقول الواجهة
        amount = float(amount_entry.get())
        category = category_combo.get()
        description = desc_entry.get()

        if amount <= 0:
            messagebox.showerror("خطأ", "يجب أن تكون قيمة المبلغ موجبة.")
            return

        # تحديث البيانات
        total_balance -= amount
        expense_list.append((description, category, amount))

        # تحديث الواجهة
        update_display()
        
        # مسح حقول الإدخال
        amount_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)
        category_combo.set('') # مسح القائمة المنسدلة
        
        messagebox.showinfo("نجاح", "تمت إضافة النفقة بنجاح.")

    except ValueError:
        messagebox.showerror("خطأ", "الرجاء إدخال رقم صحيح للمبلغ.")

def update_display():
    """تحديث عرض الرصيد الإجمالي وقائمة النفقات."""
    
    # تحديث الرصيد الإجمالي
    balance_var.set(f"الرصيد المتبقي: {total_balance:,.2f} ريال")
    
    # تحديث قائمة النفقات
    for i in expense_tree.get_children():
        expense_tree.delete(i) # مسح القائمة القديمة

    for desc, cat, amt in expense_list:
        expense_tree.insert("", tk.END, values=(desc, cat, f"{amt:,.2f}"))

# --- إعداد الواجهة الرسومية (GUI Setup) ---

# تهيئة النافذة الرئيسية
app = tk.Tk()
app.title("📊 نظام تتبع الميزانية (Mockup)")
app.geometry("800x550")
app.config(bg="#f4f4f9") # لون خلفية فاتح

# تصميم الخطوط والألوان
HEADER_FONT = ('Arial', 18, 'bold')
LABEL_FONT = ('Arial', 10)
BUTTON_STYLE = {'bg': '#007bff', 'fg': 'white', 'font': ('Arial', 10, 'bold'), 'relief': tk.FLAT}

# --- الجزء العلوي: لوحة الرصيد الإجمالي ---
balance_frame = tk.Frame(app, bg="#ffffff", padx=20, pady=15, relief=tk.RAISED, borderwidth=1)
balance_frame.pack(fill='x', padx=10, pady=10)

balance_var = tk.StringVar(value=f"الرصيد المتبقي: {total_balance:,.2f} ريال")
balance_label = tk.Label(balance_frame, textvariable=balance_var, font=HEADER_FONT, fg="#28a745", bg="#ffffff")
balance_label.pack(fill='x')

# --- الجزء الأوسط: إضافة نفقة جديدة ---
input_frame = tk.LabelFrame(app, text="➕ إضافة نفقة جديدة", font=('Arial', 12, 'bold'), bg="#f4f4f9", padx=10, pady=10)
input_frame.pack(fill='x', padx=10, pady=10)

# حقل المبلغ
tk.Label(input_frame, text="المبلغ (ريال):", font=LABEL_FONT, bg="#f4f4f9").grid(row=0, column=0, padx=5, pady=5, sticky='w')
amount_entry = tk.Entry(input_frame, font=LABEL_FONT, width=15)
amount_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

# حقل الوصف
tk.Label(input_frame, text="الوصف:", font=LABEL_FONT, bg="#f4f4f9").grid(row=1, column=0, padx=5, pady=5, sticky='w')
desc_entry = tk.Entry(input_frame, font=LABEL_FONT, width=30)
desc_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

# حقل الفئة (القائمة المنسدلة)
tk.Label(input_frame, text="الفئة:", font=LABEL_FONT, bg="#f4f4f9").grid(row=0, column=2, padx=10, pady=5, sticky='w')
categories = ['طعام وشراب', 'مواصلات', 'إيجار/فواتير', 'تسوق', 'أخرى']
category_combo = ttk.Combobox(input_frame, values=categories, font=LABEL_FONT, width=15)
category_combo.grid(row=0, column=3, padx=5, pady=5, sticky='w')
category_combo.set(categories[0]) # تعيين قيمة افتراضية

# زر الإضافة
add_button = tk.Button(input_frame, text="إضافة النفقة", command=add_expense, **BUTTON_STYLE)
add_button.grid(row=1, column=3, columnspan=1, padx=10, pady=5, sticky='e')

# --- الجزء السفلي: عرض قائمة النفقات ---
list_frame = tk.LabelFrame(app, text="📋 سجل النفقات الأخيرة", font=('Arial', 12, 'bold'), bg="#f4f4f9", padx=10, pady=5)
list_frame.pack(fill='both', expand=True, padx=10, pady=10)

# جدول (Treeview) لعرض النفقات
cols = ('الوصف', 'الفئة', 'المبلغ')
expense_tree = ttk.Treeview(list_frame, columns=cols, show='headings')

# تنسيق الأعمدة
for col in cols:
    expense_tree.heading(col, text=col)
    expense_tree.column(col, anchor=tk.CENTER, width=150)