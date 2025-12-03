# -*- coding: utf-8 -*-
"""
BIGWIN959 - 125% Cricket Activity Bot Flow (v2)
- 顶部变量统一配置 URL / file_id
- 从第二阶段开始，每一步都提供：
  - 返回上一层
  - Contact Support
"""

# ===================== 可配置变量（全部留空，等你填） =====================

REGISTER_URL = "https://channel2.bigwin959.com/register.html"        # 注册页面 URL
ANDROID_APP_URL = "https://images.738382910483.com/wsd-images-prod/bigbdtf7/app_pack/android/bigbdtf7_2.4.76_20251105095117.apk"     # Android APP 下载链接
IOS_APP_URL = "https://images.738382910483.com/wsd-images-prod/bigbdtf7/app_pack/mobileconfig/bigbdtf7_2.4.3_20251105095116.mobileconfig"         # iOS APP 下载链接

WHATSAPP_URL = "https://wa.me/qr/Y5LGYED5VPXZE1"        # WhatsApp 客服链接
TELEGRAM_SUPPORT_BOT_URL = "https://t.me/Superbigwin959_bot"  # Telegram 客服 Bot 链接

TOPUP_URL = "https://channel4.bigwin959.com/register.html"           # 网站充值 / 加余额页面 URL

CRICKET_STEPS_FILE_ID = "AgACAgUAAxkBAAMdaS8GSrppB7wM7B1G90eUi6CsFrgAAl4Maxuc3XlVmRmu0s87bekBAAMCAAN5AAM2BA"  # 你那张 “৩ ধাপ ১২৫% ক্রিকেট আপগ্রেড” 图片的 file_id


# ===================== 下面开始是逻辑代码 =====================

import os
from dotenv import load_dotenv


from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ========== CONFIG ==========
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

application = ApplicationBuilder().token(BOT_TOKEN).build()  # ← 换成你的 Bot Token


# callback_data 常量
CB_NEW_USER = "nu"              # 新用户
CB_REGISTERED_USER = "ru"       # 已注册

CB_NU_DETAILS = "nu_details"    # 新用户 - 查看 125% 详情（NU2）
CB_NU_DOWNLOAD = "nu_download"  # 新用户 - 下载 APP（从 NU1）
CB_NU_SUPPORT = "nu_support"    # 新用户 - 客服（从 NU1）

CB_NU_DETAILS_REGISTER = "nu_details_register"
CB_NU_DETAILS_DOWNLOAD = "nu_details_download"
CB_NU_DETAILS_SUPPORT = "nu_details_support"

CB_BACK_TO_NU1 = "back_nu1"
CB_BACK_TO_NU2 = "back_nu2"

CB_RU_YES_BAL = "ru_yes_bal"    # 已注册 - 已经加过余额
CB_RU_NO_BAL = "ru_no_bal"      # 已注册 - 还没加过余额
CB_RU_SUPPORT = "ru_support"    # 已注册 - 联系客服（从 YES）
CB_RU_TOPUP = "ru_topup"        # 已注册 - 去加余额（从 NO）
CB_BACK_TO_RU1 = "back_ru1"


# ============= 一些复用的小工具函数，方便“返回上一页” =============

def new_user_menu_keyboard() -> InlineKeyboardMarkup:
    """NU1 的按钮"""
    keyboard = [
        [InlineKeyboardButton("✅ ১২৫% ক্রিকেট অফার বিস্তারিত", callback_data=CB_NU_DETAILS)],
        [InlineKeyboardButton("📱 অ্যাপ ডাউনলোড গাইড", callback_data=CB_NU_DOWNLOAD)],
        [InlineKeyboardButton("💬 কাস্টমার সাপোর্ট", callback_data=CB_NU_SUPPORT)],
    ]
    return InlineKeyboardMarkup(keyboard)


def new_user_menu_text() -> str:
    """NU1 的文字"""
    return (
        "দারুণ! 🏏  \n\n"
        "নতুন ব্যবহারকারীদের জন্য এখন চলছে\n"
        "“১২৫% ক্রিকেট অ্যাক্টিভিটি আপগ্রেড”\n"
        "+ কিছু extra সুবিধা।\n\n"
        "এখন আপনি কী করতে চান?"
    )


def nu2_summary_keyboard() -> InlineKeyboardMarkup:
    """NU2 总结页按钮"""
    keyboard = [
        [InlineKeyboardButton("🚀 এখনই রেজিস্টার করুন", callback_data=CB_NU_DETAILS_REGISTER)],
        [InlineKeyboardButton("📱 অ্যাপ ডাউনলোড", callback_data=CB_NU_DETAILS_DOWNLOAD)],
        [InlineKeyboardButton("💬 সাপোর্টে মেসেজ করুন", callback_data=CB_NU_DETAILS_SUPPORT)],
        [InlineKeyboardButton("🔙 আগের ধাপে ফিরুন", callback_data=CB_BACK_TO_NU1)],
    ]
    return InlineKeyboardMarkup(keyboard)


def nu2_summary_text() -> str:
    """NU2 总结页文字"""
    return (
        "✔️ এই ৩টি ধাপ শেষ হলে\n"
        "আপনার জন্য ১২৫% ক্রিকেট আপগ্রেড,\n"
        "স্পেশাল স্পিন অফার এবং অতিরিক্ত গেম ক্রেডিট গাইড আনলক হবে।\n\n"
        "পরবর্তী ধাপ বেছে নিন:"
    )


def ru1_menu_text() -> str:
    """RU1 文本"""
    return (
        "স্বাগতম ফিরে আসায় ধন্যবাদ 🙌  \n\n"
        "এখান থেকে আপনি দ্রুত করতে পারেন:\n"
        "• অ্যাপ ওপেন / ডাউনলোড\n"
        "• বর্তমান ক্রিকেট অ্যাক্টিভিটি স্ট্যাটাস দেখা\n"
        "• সাপোর্টের সাথে সরাসরি চ্যাট\n\n"
        "🎁 আমাদের প্ল্যাটফর্মে রয়েছে কিছু স্পেশাল গেম ফিচার:\n"
        "• লাকি স্পিন\n"
        "• রেড প্যাকেট রেইন\n"
        "• গোল্ড ব্রেক রিওয়ার্ড\n\n"
        "👉 এগুলো সাধারণত ব্যালেন্স অ্যাক্টিভ করার পরই আনলক হয়।\n\n"
        "একটা ছোট প্রশ্ন:\n"
        "আপনি কি ব্যালেন্স যোগ করেছেন?"
    )


def ru1_menu_keyboard() -> InlineKeyboardMarkup:
    """RU1 按钮：YES / NO + 直接 Contact Support"""
    keyboard = [
        [
            InlineKeyboardButton("👍 হ্যাঁ, যোগ করেছি", callback_data=CB_RU_YES_BAL),
            InlineKeyboardButton("✋ না, এখনও যোগ করিনি", callback_data=CB_RU_NO_BAL),
        ],
        [InlineKeyboardButton("💬 কাস্টমার সাপোর্ট", callback_data=CB_RU_SUPPORT)],
    ]
    return InlineKeyboardMarkup(keyboard)


# ===================== /start 入口 =====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理 /start 命令"""
    text = (
        "স্বাগতম BIGWIN959-এ 👋\n"
        "আপনি কি নতুন, নাকি আগে থেকেই প্লেয়ার?\n\n"
        "নিচ থেকে নির্বাচন করুন:"
    )

    keyboard = [
        [
            InlineKeyboardButton("🆕 নতুন ব্যবহারকারী", callback_data=CB_NEW_USER),
            InlineKeyboardButton("🔑 ইতিমধ্যে রেজিস্টারড", callback_data=CB_REGISTERED_USER),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text=text, reply_markup=reply_markup)


# ===================== 新用户入口 =====================

async def handle_new_user(query) -> None:
    """新用户 NU1 菜单渲染（给多个地方复用）"""
    await query.edit_message_text(
        text=new_user_menu_text(),
        reply_markup=new_user_menu_keyboard(),
    )


async def cb_new_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """点击 '🆕 নতুন ব্যবহারকারী'"""
    query = update.callback_query
    await query.answer()
    await handle_new_user(query)


async def handle_nu_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """新用户：点击 '১২৫% ক্রিকেট অফার বিস্তারিত' 后，展示三步 + 图片 + 按钮"""
    query = update.callback_query
    await query.answer()

    # 文字说明 1（编辑当前消息）
    text1 = (
        "🎯 ১২৫% ক্রিকেট অ্যাক্টিভিটি আপগ্রেড পেতে\n"
        "আপনাকে শুধু ৩টি সহজ ধাপ সম্পন্ন করতে হবে:\n\n"
        "১) ফ্রি অ্যাকাউন্ট রেজিস্টার\n"
        "২) অ্যাপ ইনস্টল করে লগইন\n"
        "৩) প্রথমবার ব্যালেন্স যোগ করে ক্রিকেট অ্যাক্টিভিটিতে অংশগ্রহণ"
    )

    await query.edit_message_text(text=text1)

    # 图片（使用 file_id）
    # 图片（使用 file_id）
if CRICKET_STEPS_FILE_ID:
    try:
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=CRICKET_STEPS_FILE_ID
        )
    except Exception as e:
        print(f"Error sending photo: {e}")


    # 文字说明 2 + 按钮（新消息）
    await query.message.chat.send_message(
        text=nu2_summary_text(),
        reply_markup=nu2_summary_keyboard(),
    )


# ---- NU2 按钮：注册 / 下载 / 客服 / 返回上一层 ----

async def handle_nu_details_register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    text = (
        "ফ্রি অ্যাকাউন্ট রেজিস্টার করতে নিচের লিঙ্কে ক্লিক করুন 👇\n\n"
        f"{REGISTER_URL or '【REGISTER_URL_未配置】'}"
    )

    keyboard = [
        [InlineKeyboardButton("🔙 আগের ধাপে ফিরুন", callback_data=CB_BACK_TO_NU2)],
        [InlineKeyboardButton("💬 সাপোর্টে মেসেজ করুন", callback_data=CB_NU_DETAILS_SUPPORT)],
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_nu_details_download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    text = (
        "আপনার ফোন অনুযায়ী অ্যাপ ডাউনলোড করুন 👇\n\n"
        "📲 Android অ্যাপ:\n"
        f"{ANDROID_APP_URL or '【ANDROID_APP_URL_未配置】'}\n\n"
        "🍎 iOS অ্যাপ:\n"
        f"{IOS_APP_URL or '【IOS_APP_URL_未配置】'}"
    )

    keyboard = [
        [InlineKeyboardButton("🔙 আগের ধাপে ফিরুন", callback_data=CB_BACK_TO_NU2)],
        [InlineKeyboardButton("💬 সাপোর্টে মেসেজ করুন", callback_data=CB_NU_DETAILS_SUPPORT)],
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_nu_details_support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    text = (
        "যেকোনো সময় সাহায্য দরকার হলে এখানে মেসেজ করুন 👇\n\n"
        "📞 WhatsApp সাপোর্ট:\n"
        f"{WHATSAPP_URL or '【WHATSAPP_URL_未配置】'}\n\n"
        "🤖 Telegram সাপোর্ট BOT:\n"
        f"{TELEGRAM_SUPPORT_BOT_URL or '【TELEGRAM_SUPPORT_BOT_URL_未配置】'}"
    )

    keyboard = [
        [InlineKeyboardButton("🔙 আগের ধাপে ফিরুন", callback_data=CB_BACK_TO_NU2)],
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_back_to_nu2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """返回 NU2 总结页"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=nu2_summary_text(),
        reply_markup=nu2_summary_keyboard(),
    )


# ---- NU1 直接 Download / Support，也要能返回 & 找客服 ----

async def handle_nu_download_direct(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    text = (
        "আপনার ফোন অনুযায়ী অ্যাপ ডাউনলোড করুন 👇\n\n"
        "📲 Android অ্যাপ:\n"
        f"{ANDROID_APP_URL or '【ANDROID_APP_URL_未配置】'}\n\n"
        "🍎 iOS অ্যাপ:\n"
        f"{IOS_APP_URL or '【IOS_APP_URL_未配置】'}"
    )

    keyboard = [
        [InlineKeyboardButton("🔙 আগের ধাপে ফিরুন", callback_data=CB_BACK_TO_NU1)],
        [InlineKeyboardButton("💬 কাস্টমার সাপোর্ট", callback_data=CB_NU_SUPPORT)],
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_nu_support_direct(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    text = (
        "যেকোনো সময় সাহায্য দরকার হলে এখানে মেসেজ করুন 👇\n\n"
        "📞 WhatsApp সাপোর্ট:\n"
        f"{WHATSAPP_URL or '【WHATSAPP_URL_未配置】'}\n\n"
        "🤖 Telegram সাপোর্ট BOT:\n"
        f"{TELEGRAM_SUPPORT_BOT_URL or '【TELEGRAM_SUPPORT_BOT_URL_未配置】'}"
    )

    keyboard = [
        [InlineKeyboardButton("🔙 আগের ধাপে ফিরুন", callback_data=CB_BACK_TO_NU1)],
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_back_to_nu1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """返回 NU1 菜单"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=new_user_menu_text(),
        reply_markup=new_user_menu_keyboard(),
    )


# ===================== 已注册用户入口 =====================

async def cb_registered_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """点击 '🔑 ইতিমধ্যে রেজিস্টারড' 显示 RU1"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=ru1_menu_text(),
        reply_markup=ru1_menu_keyboard(),
    )


async def handle_ru_yes_bal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """已注册：回答 YES（已经加过余额）"""
    query = update.callback_query
    await query.answer()

    text = (
        "ঠিক আছে! 🔍  \n\n"
        "যদি ব্যালেন্স অ্যাক্টিভ করার পরও\n"
        "১২৫% ক্রিকেট আপগ্রেড\n"
        "অথবা অন্য কোনো বিশেষ সুবিধা\n"
        "দেখা না যায়—\n\n"
        "তাহলে সরাসরি সাপোর্টকে মেসেজ দিন।\n"
        "তারা আপনার স্ট্যাটাস দেখে আপগ্রেড এবং অফারগুলো চেক করবে।\n"
    )

    keyboard = [
        [InlineKeyboardButton("💬 Contact Support", callback_data=CB_RU_SUPPORT)],
        [InlineKeyboardButton("🔙 আগের ধাপে ফিরুন", callback_data=CB_BACK_TO_RU1)],
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_ru_no_bal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """已注册：回答 NO（还没加余额）"""
    query = update.callback_query
    await query.answer()

    text = (
        "বোঝা গেল! 🔥  \n\n"
        "১২৫% ক্রিকেট অ্যাক্টিভিটি আপগ্রেড\n"
        "এবং লাকি স্পিন, রেড প্যাকেট রেইন, গোল্ড ব্রেকসহ\n"
        "সব স্পেশাল সুবিধা আনলক করতে\n"
        "প্রথমে আপনার অ্যাকাউন্টে ব্যালেন্স অ্যাক্টিভ করুন।\n\n"
        "🔗 নিচের লিঙ্কে ক্লিক করে\n"
        "ব্যালেন্স যোগ করার পেজে যান:"
    )

    keyboard = [
        [InlineKeyboardButton("🌐 ব্যালেন্স সক্রিয় করুন", callback_data=CB_RU_TOPUP)],
        [InlineKeyboardButton("💬 কাস্টমার সাপোর্ট", callback_data=CB_RU_SUPPORT)],
        [InlineKeyboardButton("🔙 আগের ধাপে ফিরুন", callback_data=CB_BACK_TO_RU1)],
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_ru_support_or_topup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """已注册：客服 or 去充值"""
    query = update.callback_query
    await query.answer()

    if query.data == CB_RU_SUPPORT:
        text = (
            "📞 WhatsApp সাপোর্ট:\n"
            f"{WHATSAPP_URL or '【WHATSAPP_URL_未配置】'}\n\n"
            "🤖 Telegram সাপোর্ট BOT:\n"
            f"{TELEGRAM_SUPPORT_BOT_URL or '【TELEGRAM_SUPPORT_BOT_URL_未配置】'}"
        )
    elif query.data == CB_RU_TOPUP:
        text = (
            "ব্যালেন্স যোগ করতে এখানে ক্লিক করুন 👇\n\n"
            f"{TOPUP_URL or '【TOPUP_URL_未配置】'}"
        )
    else:
        text = "Invalid action."

    keyboard = [
        [InlineKeyboardButton("🔙 আগের ধাপে ফিরুন", callback_data=CB_BACK_TO_RU1)],
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))


async def handle_back_to_ru1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """返回 RU1 主菜单"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text=ru1_menu_text(),
        reply_markup=ru1_menu_keyboard(),
    )


# ===================== main 程序入口 =====================

def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("请先在脚本顶部填写 BOT_TOKEN")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # /start
    app.add_handler(CommandHandler("start", start))

    # 新用户 & 已注册入口
    app.add_handler(CallbackQueryHandler(cb_new_user, pattern=f"^{CB_NEW_USER}$"))
    app.add_handler(CallbackQueryHandler(cb_registered_user, pattern=f"^{CB_REGISTERED_USER}$"))

    # 新用户 NU2 + NU1 直接动作
    app.add_handler(CallbackQueryHandler(handle_nu_details, pattern=f"^{CB_NU_DETAILS}$"))
    app.add_handler(CallbackQueryHandler(handle_nu_download_direct, pattern=f"^{CB_NU_DOWNLOAD}$"))
    app.add_handler(CallbackQueryHandler(handle_nu_support_direct, pattern=f"^{CB_NU_SUPPORT}$"))

    # NU2 内部按钮
    app.add_handler(CallbackQueryHandler(handle_nu_details_register, pattern=f"^{CB_NU_DETAILS_REGISTER}$"))
    app.add_handler(CallbackQueryHandler(handle_nu_details_download, pattern=f"^{CB_NU_DETAILS_DOWNLOAD}$"))
    app.add_handler(CallbackQueryHandler(handle_nu_details_support, pattern=f"^{CB_NU_DETAILS_SUPPORT}$"))
    app.add_handler(CallbackQueryHandler(handle_back_to_nu2, pattern=f"^{CB_BACK_TO_NU2}$"))
    app.add_handler(CallbackQueryHandler(handle_back_to_nu1, pattern=f"^{CB_BACK_TO_NU1}$"))

    # 已注册分支
    app.add_handler(CallbackQueryHandler(handle_ru_yes_bal, pattern=f"^{CB_RU_YES_BAL}$"))
    app.add_handler(CallbackQueryHandler(handle_ru_no_bal, pattern=f"^{CB_RU_NO_BAL}$"))
    app.add_handler(CallbackQueryHandler(handle_ru_support_or_topup,
                                         pattern=f"^{CB_RU_SUPPORT}$|^{CB_RU_TOPUP}$"))
    app.add_handler(CallbackQueryHandler(handle_back_to_ru1, pattern=f"^{CB_BACK_TO_RU1}$"))

    print("Bot is running...（Ctrl+C 退出）")
    app.run_polling()


if __name__ == "__main__":
    main()
