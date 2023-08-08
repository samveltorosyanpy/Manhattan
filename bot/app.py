from loader import TOKEN, OWNER_BOT, dp, webhook_url
from data import config
from aiohttp import web
from aiogram import types
from src.handlers import message_handlers, commands, CallBacks
from aiogram.dispatcher.webhook import get_new_configured_app


async def on_startup(_):
    await dp.bot.set_webhook(f'{config.WEBHOOK_DOMAIN}/{TOKEN}')
    await dp.bot.send_message(chat_id=OWNER_BOT, text='Bot has been started')
    # await dp.bot.set_my_commands(
    #     types.BotCommand('start', 'Starting bot'),
    #     types.BotCommand('admin', 'Admin configs')
    # )

    CallBacks.register_message_handlers_callback(dp)
    commands.register_command_handlers(dp)
    message_handlers.register_message_handlers_new_work_day(dp)
    message_handlers.register_message_handlers_cash_box_usm_update(dp)


async def on_shutdown(_):
    await dp.bot.send_message(chat_id=OWNER_BOT, text='Bot has been stopped')


async def handle_webhook(request):
    if request.match_info.get('token') == TOKEN:
        update = types.Update(**await request.json())
        await dp.process_update(update)
        return web.Response()
    else:
        return web.Response(status=403)


if __name__ == "__main__":
    app = get_new_configured_app(dispatcher=dp, path=f'/{TOKEN}')
    app.router.add_post(f'/webhook/{TOKEN}', handle_webhook)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(
        app=app,
        host=config.WEBHOOK_HOST,
        port=config.WEBHOOK_PORT
    )
