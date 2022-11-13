# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from todoist_api_python.api import TodoistAPI


def create_todoist_task(name, description, author):
    api = TodoistAPI("todois token")
    task = api.add_task(
        content=name,
        due_string="Today",
        due_lang="en",
        description=description,
        priority=1,
        labels=[author, "telegram"]
    )
    return task.url


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def create_todoist_task_from_update(update: Update):
    text = update.effective_message.text
    info = (text[:100] + '..') if len(text) > 100 else text
    forward_author = (update.message.forward_from and (
            update.message.forward_from.full_name + " (" + update.message.forward_from.last_name + ")")) or (
                                 update.message.forward_from_chat and update.message.forward_from_chat.title)
    description = (forward_author and (forward_author + "\n")) + update.effective_message.text
    return create_todoist_task(info, description, forward_author)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task_url = create_todoist_task_from_update(update)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=task_url)


if __name__ == '__main__':
    application = ApplicationBuilder().token("telegram_bot_token").build()

    # start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler((filters.TEXT & (~filters.COMMAND)), echo)
    # application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
