کد اصلی در code.py نوشته شده است.
برای دیدن خروجی که من گرفتم می تونید فایل out رو بررسی کنید :)
--------------------------------------------------------------------------------------------------------
برای اینکه خودتون پروژه رو ران کنید ابتدا در دایرکتوری اصلی پروژه با دستور 
sudo docker run -t -i -p 5000:5000 -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-routed --algorithm mld /data/iran-latest.osrm
یک http server می سازید.
حال باید کتابخونه های لازم رو نصب کنید
pip install requests 
pip install geopy
سپس با رفتن به دایرکتوری 2 و اجرای دستور 
python3 code.py < challenge.txt > out
می تونید خروجی متنی را در فایل out ببینید.

---------------
در صورت مشکل
برای build کردن osrm میتونید از دستورات زیر در دایرکتوری اصلی پروژه استفاده کنید:
sudo docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-extract -p /opt/car.lua /data/iran-latest.osm.pbf || echo "osrm-extract failed"
sudo docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-partition /data/iran-latest.osrm || echo "osrm-partition failed"
sudo docker run -t -v "${PWD}:/data" ghcr.io/project-osrm/osrm-backend osrm-customize /data/iran-latest.osrm || echo "osrm-customize failed"

ولی نیازی به این کار نیست چون فایل های build شده در دایرکتوری اصلی پروژه قرار گرفتند. (در صورت نیاز و مشکل دستورات بالا را برای build کردن ران کنید :))

-----------------------------------------------------------------------------------------------------------------------------------------------------------------
توضیح الگوریتم:
من ابتدا با استفاده از osrm لوکیشن هر گزارش رو به نزدیک ترین خیابون(اتوبان و ...) تبدیل کردم با دستور nearest در خود osrm.
سپس هر دو گزارشی که فاصلشون حداکثر ۴۵۰ متر بود رو در یک گروه قرار دادم
در هر گروه که شامل چندین گزارش هست خیابونی رو انتخاب می کنم که بیشترین تعداد گزارش در اون گروه مربوط به اون خیابون هست. فرض کنید خیابون A
حالا میانگین X , Y های همه گزارش هایی که در خیابون A هستند رو محاسبه کرده و به عنوان حدس خروجی میدم
و در هر زمان که اختلاف اخرین تایم حضور هر پلیس با تایم فعلی بیشتر از ۳۶۰۰ ثانیه شد پلیس مدنظر را حذف می کنم.






