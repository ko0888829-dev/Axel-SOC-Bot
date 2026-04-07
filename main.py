import telebot
from telebot import types
import sqlite3

# --- ပြင်ဆင်ရန် အချက်အလက်များ ---
API_TOKEN = '8776335987:AAE98KHB9cD2Fpznsz93IMl5oK3oB94-D3I'
ADMIN_ID = 8440467550 
CHANNEL_USERNAME = '@Axel_X_H'
# ----------------------------

bot = telebot.TeleBot(API_TOKEN)

def init_db():
    conn = sqlite3.connect('axel_shop.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)')
    conn.commit()
    conn.close()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    conn = sqlite3.connect('axel_shop.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

    welcome_text = (
        "👋 **Xi, Axel SOC Shop မှ ကြိုဆိုပါတယ်** ✨\n\n"
        "လိုအပ်သော ဝန်ဆောင်မှုများကို အောက်ပါ ခလုတ်များတွင် ရွေးချယ်နိုင်သည်ဗျ။\n\n"
        "ဝယ်ယူရန် @RAM_10_01 ကို တိုက်ရိုက်ဆက်သွယ်ပါ"
    )
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("💎 MLBB Diamonds", callback_data="mlbb")
    btn2 = types.InlineKeyboardButton("🚀 Social Boosts", callback_data="social")
    btn3 = types.InlineKeyboardButton("👨‍💻 Admin ဆက်သွယ်ရန်", url="https://t.me/RAM_10_01")
    
    markup.add(btn1, btn2)
    markup.add(btn3)
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "mlbb":
        dia_list = (
            "🎮 **MLBB Diamond Price List**\n"
            "━━━━━━━━━━━━━━━\n"
            "💎 11 - 1000ks | 💎 22 - 2000ks\n"
            "💎 56 - 4550ks | 💎 86 - 6300ks\n"
            "💎 172 - 12500ks | 💎 257 - 16300ks\n"
            "💎 343 - 23500ks | 💎 429 - 27700ks\n"
            "💎 514 - 32800ks | 💎 600 - 39400ks\n"
            "💎 706 - 45800ks | 💎 878 - 54500ks\n"
            "💎 963 - 59500ks | 💎 1135 - 69000ks\n"
            "💎 1412 - 84500ks | 💎 2195 - 115000ks\n"
            "💎 2452 - 133500ks | 💎 2901 - 193500ks\n"
            "💎 3688 - 239000ks | 💎 5532 - 349000ks\n"
            "💎 7376 - 456000ks | 💎 9288 - 554000ks\n\n"
            "🔥 **Diamond 2X PROMO**\n"
            "💎 50+50 - 3800ks\n"
            "💎 150+150 - 11400ks\n"
            "💎 250+250 - 19000ks\n"
            "💎 500+500 - 38000ks\n"
            "━━━━━━━━━━━━━━━\n"
            "✅ ဝယ်ယူရန် @RAM_10_01"
        )
        bot.send_message(call.message.chat.id, dia_list, parse_mode="Markdown")
        
    elif call.data == "social":
        social_list = (
            "📣 **Social Boost Service**\n"
            "━━━━━━━━━━━━━━━\n"
            "📱 **TikTok Services (မြန်မာလူအစစ်)**\n"
            "- Likes 1k - 3000ks\n"
            "- View 10k - 3500ks\n"
            "- Likes 1k + View 5k - 4500ks\n"
            "- Likes 5k + View 10k - 8000ks\n"
            "- Followers 1k - 25000ks\n\n"
            "✈️ **Telegram Services**\n"
            "- Channel Sub 1k - 15000ks\n"
            "- Channel Sub 10k - 130,000ks (🎁 500 Sub Free)\n"
            "- Post Reaction 1k - 3000ks\n\n"
            "⏳ Wait time: 5 Minutes\n"
            "✅ အာမခံ (ပြန်မကျ/တစ်သက်စာ)\n"
            "━━━━━━━━━━━━━━━\n"
            "✅ ဝယ်ယူရန် @RAM_10_01"
        )
        bot.send_message(call.message.chat.id, social_list, parse_mode="Markdown")

if __name__ == '__main__':
    init_db()
    bot.infinity_polling()
