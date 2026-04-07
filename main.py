import telebot
from telebot import types
import io

# --- Configuration ---
API_TOKEN = '8776335987:AAE98KHB9cD2Fpznsz93IMl5oK3oB94-D3I' 
ORDER_BOT_TOKEN = '8625083982:AAE98KHB9cD2Fpznsz93IMl5oK3oB94-D3I' 
ADMIN_ID = 8440467550 

bot = telebot.TeleBot(API_TOKEN)
order_bot = telebot.TeleBot(ORDER_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("💎 MLBB Diamonds ဝယ်ယူရန်", callback_data="order_mlbb"),
        types.InlineKeyboardButton("🚀 Social Boost Services", callback_data="order_social")
    )
    bot.send_message(message.chat.id, "👋 **Axel SOC Shop မှ ကြိုဆိုပါတယ်**", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data in ["order_mlbb", "order_social"]:
        msg = bot.send_message(call.message.chat.id, "📸 ပြေစာ Screenshot ပုံကိုပို့ပြီး **Caption** မှာ ID/Link ကို တစ်ခါတည်းတွဲရေးပေးပါဗျ။")
        bot.register_next_step_handler(msg, process_final_order)

def process_final_order(message):
    if message.content_type != 'photo':
        msg = bot.send_message(message.chat.id, "⚠️ ကျေးဇူးပြု၍ **ပုံနဲ့စာသားကို တွဲပို့ပေးပါ**။")
        bot.register_next_step_handler(msg, process_final_order)
        return
    
    caption_text = message.caption if message.caption else "No details"
    admin_info = f"📩 **Order New!**\n👤 From: {message.from_user.first_name} (@{message.from_user.username})\n📝 Info: {caption_text}"

    try:
        # File ID ပြဿနာကို ကျော်လွှားရန် ပုံကို download အရင်ဆွဲပါမယ်
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Admin Bot ကနေ ပုံကို ပြန်ပို့ပေးပါမယ်
        photo_stream = io.BytesIO(downloaded_file)
        order_bot.send_photo(ADMIN_ID, photo_stream, caption=admin_info)
        
        bot.send_message(message.chat.id, "ဝယ်ယူအားပေးမှုကိုကျေးဇူးအထူတင်ရှိပါသည်😘")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Error: {str(e)}")

if __name__ == '__main__':
    bot.infinity_polling()
    
