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

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = "👋 **Axel SOC Shop မှ ကြိုဆိုပါတယ်** ✨\n\nဝယ်ယူလိုသည့် အမျိုးအစားကို ရွေးချယ်ပါ သို့မဟုတ် Admin ကို ဆက်သွယ်ပါဗျ။"
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("💎 MLBB Diamonds ဝယ်ယူရန်", callback_data="buy_mlbb"),
        types.InlineKeyboardButton("🚀 Social Boost Services", callback_data="buy_social"),
        types.InlineKeyboardButton("👨‍💻 Admin ဆက်သွယ်ရန်", url=f"https://t.me/{ADMIN_USERNAME.replace('@','')}")
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_buy(call):
    if call.data == "buy_mlbb":
        user_orders[call.message.chat.id] = {'type': 'MLBB Diamond'}
        msg = bot.send_message(call.message.chat.id, "🎮 **MLBB Player ID + Zone ID** ကို ရိုက်ထည့်ပေးပါဗျ။\n(ဥပမာ - 12345678 1234)", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_details)
    
    elif call.data == "buy_social":
        user_orders[call.message.chat.id] = {'type': 'Social Boost'}
        msg = bot.send_message(call.message.chat.id, "🚀 **Boost လုပ်မဲ့ Link** ကို ထည့်ပေးပါဗျ။\n\n⚠️ *သတိပေးချက်: Link မှားယွင်းထည့်သွင်းပါက တာဝန်ယူမည်မဟုတ်ပါ။ သေချာစွာစစ်ဆေးပေးပါ!*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_details)

def process_details(message):
    user_orders[message.chat.id]['details'] = message.text
    msg = bot.send_message(message.chat.id, "💰 **ငွေလွဲပြေစာ (Screenshot)** ကို ပေးပို့ပေးပါဗျ။", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_payment)

def process_payment(message):
    if message.content_type != 'photo':
        msg = bot.send_message(message.chat.id, "⚠️ ကျေးဇူးပြု၍ ဓာတ်ပုံ (Screenshot) သာ ပေးပို့ပေးပါဗျ။")
        bot.register_next_step_handler(msg, process_payment)
        return

    order = user_orders[message.chat.id]
    photo_id = message.photo[-1].file_id
    
    # Admin Bot ဆီ Order ပို့ခြင်း
    admin_notif = (
        f"📩 **Order အသစ်ရောက်ရှိလာပါပြီ**\n\n"
        f"👤 **Customer:** {message.from_user.first_name} (@{message.from_user.username})\n"
        f"📦 **အမျိုးအစား:** {order['type']}\n"
        f"📝 **အချက်အလက်:** `{order['details']}`\n\n"
        f"📌 *ငွေလွဲပြေစာကို အောက်တွင် ကြည့်ရှုနိုင်ပါသည်။*"
    )
    
    try:
        order_bot.send_photo(ADMIN_ID, photo_id, caption=admin_notif, parse_mode="Markdown")
        bot.send_message(message.chat.id, "✅ **Order တင်ခြင်း အောင်မြင်ပါသည်**\n\nAdmin မှ စစ်ဆေးပြီးပါက ဝန်ဆောင်မှုပေးပါလိမ့်မည်။ ခေတ္တစောင့်ဆိုင်းပေးပါဗျ။", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Order တင်ရာတွင် အမှားအယွင်းရှိခဲ့သည်။ Admin သို့ တိုက်ရိုက် ဆက်သွယ်ပေးပါဗျ။")

if __name__ == '__main__':
    bot.infinity_polling()
