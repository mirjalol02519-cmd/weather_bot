# Ob-havo bot
---

### Bot nima qila oladi ?
- Dunyoning istalgan shahridagi ob-havo ma'lumotini qaytaradi
- Ob-havo ma'lumotlaridan kelib chiqib, maslahat beradi
- Ko'p so'raladigan shaharlarni saqlash imkoniyati
- Foydalanuvchilarni eslab qolish imkoniyati

### Qanday ishga tushirsa bo'ladi ?
1. Loyihani yuklab olish
---
2. Virtual muhit yaratish:
```bash
# Windows
python -m venv .venv

# MacOS / Linux
python3 -m venv .venv
```

---
3. Virtual muhitni aktivlashtirish:
```bash
# Windows
.venv\Scripts\Activate

# MacOS / Linux
source .venv/bin/activate
```
---
4. Virtual muhitga kerakli kutubxonalarni o'rnatish:
```bash
pip install -r requirements.txt
```
---
4. `.env` faylini yaratish va uni ichiga quyidagi o'zgarmaslar uchun qiymat yozish
```
WEATHER_TOKEN=
BOT_TOKEN=

ADMINS=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=
DB_HOST=
```
---
4. Botni ishga tushirish
```bash
python main.py
```
# weather_bot
