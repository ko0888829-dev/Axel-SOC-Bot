import telebot
from telebot import types

# --- Configuration ---
API_TOKEN = '8776335987:AAE98KHB9cD2Fpznsz93IMl5oK3oB94-D3I' # User Bot
ORDER_BOT_TOKEN = '8625083982:AAFgr2_WMtyr5eQjxKUZW2H5331NyXcbVAY' # Admin Bot
# အောက်က ADMIN_ID ကို သင့်ရဲ့ ID အစစ်အမှန်နဲ့ သေချာပြန်လဲပေးပါ
ADMIN_ID = 8440467550 

bot = telebot.TeleBot(API_TOKEN)
order_bot = telebot.TeleBot(ORDER_BOT_TOKEN)

# --- Menu Helper ---
def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("💎 MLBB Diamonds ဝယ်ယူရန်", callback_data="list_mlbb"),
        types.InlineKeyboardButton("🚀 Social Boost Services", callback_data="list_social")
    )
    bot.send_message(chat_id, "👋 **Axel SOC Shop မှ ကြိုဆိုပါတယ်**", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    show_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "list_mlbb":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛒 Order တင်ရန်", callback_data="order_mlbb"))
        bot.edit_message_text("🎮 **MLBB Diamond ဈေးနှုန်းများ**", call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    elif call.data == "order_mlbb":
        msg = bot.send_message(call.message.chat.id, 
            "ပြေစာssနဲ့ဝယ်ယူမည့်ပစ္စည်းအမျိုးအစားserver idကိုတစ်ခါထည်းတွဲပို့ပေးပါ\n\n"
            "❗❗ Server idကိုသေချာစစ်ဆေးပါ\n"
            "မှားယွင်းပါက𝘼𝙭𝙚𝙡 𝙎𝙊𝘾 𝙎𝙝𝙤𝙥မှတာဝန်ယူမည်မဟုတ်ပါ")
        bot.register_next_step_handler(msg, process_order)

    elif call.data == "list_social":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛒 Order တင်ရန်", callback_data="order_social"))
        bot.edit_message_text("🚀 **Social Boost Services**", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "order_social":
        msg = bot.send_message(call.message.chat.id, 
            "ပြေစာssနဲ့ဝယ်ယူမည့်ပစ္စည်းအမျိုးအစားတစ်ခါတည်းတွဲပို့ပေးရမှာ\n"
            "Linkကို‌သေချာစစ်‌ဆေးပေးပါ")
        bot.register_next_step_handler(msg, process_order)

def process_order(message):
    if message.content_type != 'photo':
        msg = bot.send_message(message.chat.id, "⚠️ ပြေစာ Screenshot ပုံနဲ့ အချက်အလက်ကို တွဲပို့ပေးပါဗျ။")
        bot.register_next_step_handler(msg, process_order)
        return

    photo_id = message.photo[-1].file_id
    details = message.caption if message.caption else "No Details"
    
    try:
        # Admin Bot ကနေ သင့်ဆီ တန်းပို့ပေးမယ့်အပိုင်း
        order_bot.send_photo(ADMIN_ID, photo_id, caption=f"📩 **Order New**\nFrom: @{message.from_user.username}\nDetails: {details}")
        bot.send_message(message.chat.id, "ဝယ်ယူအားပေးမှုကိုကျေးဇူးအထူတင်ရှိပါသည်😘")
    except Exception as e:
        # Error အတိအကျသိရအောင် error message ပြခိုင်းထားတယ်
        bot.send_message(message.chat.id, f"⚠️ Admin Bot သို့ ပို့၍မရပါ။ Error: {str(e)}")

bot.infinity_polling()
