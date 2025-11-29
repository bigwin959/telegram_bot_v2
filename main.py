# pip install python-telegram-bot==21.4

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ========== CONFIG ==========
BOT_TOKEN = "8141858152:AAFK9PuN1cdy59l_xDM_pU68iMW_iKXFQZ8"  # ← 换成你的 Bot Token

# 你的 guide-book HTML 页面地址
GUIDE_URL = "https://fsguidebook.netlify.app/"  # ← 换成实际链接


def build_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                # 按钮文字：孟加拉语版本的 “Get 20 Free Spins + 200 BDT”
                "🎁 ২০ ফ্রি স্পিন + ২০০ টাকা গাইড খুলুন",
                url=GUIDE_URL,
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 文案尽量短，只告诉他“点下面按钮”
    text = (
        "🎁 *Get 20 Free Spins + 200 BDT*\n\n"
        "নীচের বাটনে ক্লিক করুন, সম্পূর্ণ বাংলা গাইড খুলে যাবে 👇"
    )

    await (update.message or update.callback_query.message).reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=build_keyboard(),
        disable_web_page_preview=True,
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Simple guide-link bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
