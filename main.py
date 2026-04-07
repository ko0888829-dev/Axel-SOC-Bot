import telebot
from telebot import types

# --- Configuration ---
API_TOKEN = '8776335987:AAE98KHB9cD2Fpznsz93IMl5oK3oB94-D3I' # User သုံးမဲ့ Bot
ORDER_BOT_TOKEN = '8649013071:AAFMtmBe0r6wLvyqhxn0ggctoy6Tep9Gh4E' # Order လက်ခံမဲ့ Bot
ADMIN_ID = 8440467550 
ADMIN_USERNAME = "@Axel_X_H"

bot = telebot.TeleBot(API_TOKEN)
order_bot = telebot.TeleBot(ORDER_BOT_TOKEN)

user_orders = {}

# --- ဈေးနှုန်းစာရင်းများ ---
ML_PRICE = (
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
    "━━━━━━━━━━━━━━━"
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
    "- Channel Sub 10k - 130,000ks (🎁 500 Sub Free)\n"
    "- Post Reaction 1k - 3000ks\n\n"
    "⏳ Wait time: 5 Minutes\n"
    "✅ အာမခံ (ပြန်မကျ/တစ်သက်စာ)\n"
    "━━━━━━━━━━━━━━━"
)

@bot.message_handler(commands=['start'])
def start(message):
    show_main_menu(message.chat.id)

def show_main_menu(chat_id):
    welcome_text = "👋 **Axel SOC Shop မှ ကြိုဆိုပါတယ်** ✨\n\nဝယ်ယူလိုသည့် အမျိုးအစားကို ရွေးချယ်ပါ သို့မဟုတ် Admin ကို ဆက်သွယ်ပါဗျ။"
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("💎 MLBB Diamonds ဝယ်ယူရန်", callback_data="list_mlbb"),
        types.InlineKeyboardButton("🚀 Social Boost Services", callback_data="list_social"),
        types.InlineKeyboardButton("👨‍💻 Admin ဆက်သွယ်ရန်", url=f"https://t.me/{ADMIN_USERNAME.replace('@','')}")
    )
    bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "list_mlbb":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛒 Order တင်ရန်", callback_data="order_mlbb"))
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
        bot.edit_message_text(ML_PRICE, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "list_social":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛒 Order တင်ရန်", callback_data="order_social"))
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
        bot.edit_message_text(SOCIAL_PRICE, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "main_menu":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        show_main_menu(call.message.chat.id)

    elif call.data == "order_mlbb":
        user_orders[call.message.chat.id] = {'type': 'MLBB Diamond'}
        msg = bot.send_message(call.message.chat.id, "🎮 **ဝယ်ယူမည့်အမျိုးအစား** နှင့် **Player ID + Zone ID** ကိုတွဲရေးပြီး တစ်ခါတည်း ပို့ပေးပါဗျ။\n\n❗❗ **Server ID ကိုသေချာစွာစစ်ဆေးပေးပါ**", parse_mode="Markdown")
        bot.register_next_step_handler(msg, ask_receipt)

    elif call.data == "order_social":
        user_orders[call.message.chat.id] = {'type': 'Social Boost'}
        msg = bot.send_message(call.message.chat.id, "🚀 **ဝယ်ယူမည့်အမျိုးအစား** နှင့် **Link** ကိုတွဲရေးပြီး တစ်ခါတည်း ပို့ပေးပါဗျ။", parse_mode="Markdown")
        bot.register_next_step_handler(msg, ask_receipt)

def ask_receipt(message):
    user_orders[message.chat.id]['details'] = message.text
    msg = bot.send_message(message.chat.id, "💰 **ငွေလွဲပြေစာ (Screenshot)** ကို ပေးပို့ပေးပါဗျ။", parse_mode="Markdown")
    bot.register_next_step_handler(msg, final_process)

def final_process(message):
    if message.content_type != 'photo':
        msg = bot.send_message(message.chat.id, "⚠️ ကျေးဇူးပြု၍ ပြေစာ Screenshot (ဓာတ်ပုံ) ကို ပေးပို့ပေးပါဗျ။")
        bot.register_next_step_handler(msg, final_process)
        return

    order = user_orders[message.chat.id]
    photo_id = message.photo[-1].file_id
    
    # Admin Bot ဆီ Order ပို့ခြင်း
    admin_notif = (
        f"📩 **Order အသစ်ရောက်ရှိလာပါပြီ**\n\n"
        f"👤 **Customer:** {message.from_user.first_name} (@{message.from_user.username})\n"
        f"📦 **အမျိုးအစား:** {order['type']}\n"
        f"📝 **အချက်အလက်:** `{order['details']}`"
    )
    
    try:
        order_bot.send_photo(ADMIN_ID, photo_id, caption=admin_notif, parse_mode="Markdown")
        bot.send_message(message.chat.id, "ဝယ်ယူအားပေးမှုကိုကျေးဇူးအထူတင်ရှိပါသည်😘", parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, "⚠️ Admin Bot သို့ ပေးပို့ရာတွင် အမှားရှိနေပါသည်။ Admin ဆီ တိုက်ရိုက်ပြောပေးပါဗျ။")

if __name__ == '__main__':
    bot.infinity_polling()
