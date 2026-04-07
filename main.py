import telebot
from telebot import types
import io

# --- Configuration ---
API_TOKEN = '8776335987:AAE98KHB9cD2Fpznsz93IMl5oK3oB94-D3I' 
ORDER_BOT_TOKEN = '8625083982:AAFgr2_WMtyr5eQjxKUZW2H5331NyXcbVAY' 
ADMIN_ID = 8440467550 

# Admin Username ကို @Axel_X_H သို့ ပြောင်းလဲသတ်မှတ်ခြင်း
ADMIN_USERNAME = "Axel_X_H" 

bot = telebot.TeleBot(API_TOKEN)
order_bot = telebot.TeleBot(ORDER_BOT_TOKEN)

# --- Price Lists ---
ML_PRICE = (
    "🎮 **MLBB Diamond Price List**\n"
    "━━━━━━━━━━━━━━━\n"
    "💎 11 - 1000ks\n"
    "💎 22 - 2000ks\n"
    "💎 56 - 4550ks\n"
    "💎 86 - 6300ks\n"
    "💎 172 - 12500ks\n"
    "💎 257 - 16300ks\n"
    "💎 343 - 23500ks\n"
    "💎 429 - 27700ks\n"
    "💎 514 - 32800ks\n"
    "💎 600 - 39400ks\n"
    "💎 706 - 45800ks\n"
    "💎 878 - 54500ks\n"
    "💎 963 - 59500ks\n"
    "🔥 **Diamond 2X PROMO**\n"
    "💎 50+50 - 3800ks\n"
    "💎 150+150 - 11400ks\n"
    "💎 250+250 - 19000ks\n"
    "💎 500+500 - 38000ks\n"
    "Weekly pass - 6500ks\n"
    "━━━━━━━━━━━━━━━\n"
    "diamond 1kနှင့်အထက်ဝယ်ယူရန် Contact Admin"
)

SOCIAL_PRICE = (
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
    "- Channel Sub 10k - 130,000ks\n"
    "- Post Reaction 1k - 3000ks\n\n"
    "✅ အာမခံ (ပြန်မကျ/တစ်သက်စာ)\n"
    "━━━━━━━━━━━━━━━"
)

@bot.message_handler(commands=['start'])
def start(message):
    show_main_menu(message.chat.id)

def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("💎 MLBB Diamonds ဝယ်ယူရန်", callback_data="list_mlbb"),
        types.InlineKeyboardButton("🚀 Social Boost Services", callback_data="list_social"),
        # Link ကို @Axel_X_H သို့ ချိတ်ဆက်ပေးထားပါတယ်
        types.InlineKeyboardButton("👨‍💻 Admin ဆက်သွယ်ရန်", url=f"https://t.me/{ADMIN_USERNAME}")
    )
    bot.send_message(chat_id, "👋 **Axel SOC Shop မှ ကြိုဆိုပါတယ်** ✨\n\nဝယ်ယူလိုသည့် အမျိုးအစားကို ရွေးချယ်ပါ သို့မဟုတ် Admin ကို ဆက်သွယ်ပါဗျ။", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "list_mlbb":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛒 Order တင်ရန်", callback_data="order_process"))
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
        bot.edit_message_text(ML_PRICE, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        
    elif call.data == "list_social":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛒 Order တင်ရန်", callback_data="order_process"))
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
        bot.edit_message_text(SOCIAL_PRICE, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        
    elif call.data == "main_menu":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)
        
    elif call.data == "order_process":
        msg = bot.send_message(call.message.chat.id, "📸 ပြေစာ Screenshot ပုံကိုပို့ပြီး **Caption** မှာ ID/Link ကို တစ်ခါတည်းတွဲရေးပေးပါဗျ။")
        bot.register_next_step_handler(msg, process_final_order)

def process_final_order(message):
    if message.content_type != 'photo':
        msg = bot.send_message(message.chat.id, "⚠️ ကျေးဇူးပြု၍ ပုံနဲ့စာသားကို တွဲပို့ပေးပါဗျ။")
        bot.register_next_step_handler(msg, process_final_order)
        return
    
    caption_text = message.caption if message.caption else "No details"
    admin_info = f"📩 **Order New!**\n👤 From: {message.from_user.first_name} (@{message.from_user.username})\n📝 Info: {caption_text}"

    try:
        # File ID Error မတက်အောင် download ဆွဲပြီး ပို့ပေးခြင်း
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        photo_stream = io.BytesIO(downloaded_file)
        order_bot.send_photo(ADMIN_ID, photo_stream, caption=admin_info)
        
        bot.send_message(message.chat.id, "ဝယ်ယူအားပေးမှုကို ကျေးဇူးအထူးတင်ရှိပါသည်😘")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Error: {str(e)}")

if __name__ == '__main__':
    bot.infinity_polling()
