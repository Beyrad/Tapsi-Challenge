<div dir="rtl" style="text-align: right; font-family: 'Vazirmatn', sans-serif;">

# بخش اول

---

## توضیحات کلی پروژه و دیدن خروجی هایی که از کد گرفته شده
کد اصلی در فایل `code.py` نوشته شده و اسکریپت `gen.py` برای تبدیل ورودی سوال به فرمتی که در نقشه قابل نمایش باشد, نوشته شده.

از کد با استفاده از فایل های osrm ایرانی ران گرفته شده و خروجی ها داخل دایرکتوری `LOCAL` هستند.

خروجی‌های حاصل از اجرای `code.py` در دایرکتوری `LOCAL` ذخیره شده‌اند. با رفتن به دایرکتوری `LOCAL`، دو فایل زیر را می بینید:
- **`blue.txt`**: شامل خروجی‌ها و حدس من از گزارش‌ها.
- **`red.txt`**: شامل گزارش‌های ورودی تپسی.

برای مشاهده خروجی‌ها به‌صورت گرافیکی، در دایرکتوری `LOCAL` دستور زیر را اجرا کنید:
```bash
python3 -m http.server 8000
```
سپس در مرورگر خود آدرس `localhost:8000` یا `0.0.0.0:8000` را وارد کنید تا خروجی گرافیکی را مشاهده کنید.

---

## توضیح الگوریتم

1. ابتدا با استفاده از OSRM، لوکیشن هر گزارش را با دستور `nearest` به نزدیک‌ترین خیابان (اتوبان و غیره) تبدیل کردم.
2. گزارش‌هایی که فاصله آن‌ها حداکثر ۴۵۰ متر باشد را در یک گروه قرار دادم.
3. در هر گروه، خیابانی که بیشترین تعداد گزارش‌ها را دارد انتخاب می‌شود (مثلاً خیابان A).
4. میانگین مختصات X و Y تمام گزارش‌های مربوط به خیابان A محاسبه شده و به‌عنوان حدس خروجی ارائه می‌شود.

</div>