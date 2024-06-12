from source import *


def Main() -> None:
    AuthorizeAccounts()
    Thread(target=ProcessRequests, daemon=True).start()
    while True:
        try:
            BOT.polling(none_stop=True, interval=1)
        except Exception as e:
            Stamp(f'{e}', 'e')
            Stamp(traceback.format_exc(), 'e')


def AuthorizeAccounts():
    Stamp('Authorization procedure started', 'b')
    data = GetSector('A2', 'D500', service, 'Аккаунты', SHEET_ID)
    for account in data:
        session = os.path.join(os.getcwd(), 'sessions', f'session_{account[0]}')
        client = TelegramClient(session, account[1], account[2])
        Stamp(f'Account {account[0]}', 'i')
        try:
            password = account[3] if account[3] != '-' else None
        except IndexError:
            password = None
        client.start(phone=account[0], password=password)
        ACCOUNTS.append(client)
    Stamp('All accounts authorized', 'b')


async def PerformSubscription(link: str, amount: int, channel_type: str) -> None:
    Stamp('Subscription procedure started', 'b')
    global CUR_ACC_INDEX
    for _ in range(amount):
        acc = ACCOUNTS[CUR_ACC_INDEX]
        try:
            if channel_type == 'public':
                channel = await acc.get_entity(link)
                await acc(JoinChannelRequest(channel))
            else:
                await acc(ImportChatInviteRequest(link))
            Stamp(f"Subscribed {acc.session.filename} to {link}", 's')
        except Exception as e:
            Stamp(f"Failed to subscribe {acc.session.filename} to {link}: {e}", 'e')
        CUR_ACC_INDEX = (CUR_ACC_INDEX + 1) % len(ACCOUNTS)
        Sleep(SHORT_SLEEP, 0.5)
    Stamp('Subscription procedure finished', 'b')


def ProcessRequests() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        Stamp('Pending requests', 'i')
        for req in REQS_QUEUE:
            if datetime.now() < req['finish']:
                if req['order_type'] == 'sub':
                    duration = (req['finish'] - req['start']).total_seconds()
                    interval = duration / req['num']
                    elapsed = (datetime.now() - req['start']).total_seconds()
                    expected_subs = int(elapsed / interval)
                    current_subs = req.get('current_subs', 0)
                    subs_to_add = expected_subs - current_subs
                    if subs_to_add > 0:
                        req['current_subs'] = current_subs + subs_to_add
                        loop.run_until_complete(PerformSubscription(req['link'], subs_to_add, req['channel_type']))
            else:
                REQS_QUEUE.remove(req)
        Sleep(LONG_SLEEP)


def ChannelSub(message: telebot.types.Message) -> None:
    Stamp('Link inserting procedure', 'i')
    expected_format = r'https://t\.me/\w+'
    if not re.match(expected_format, message.text):
        BOT.send_message(message.chat.id, "❌ Ссылка на канал не похожа на корректную. "
                                          "Пожалуйста, проверьте формат ссылки (https://t.me/channel_name_or_hash)")
        BOT.register_next_step_handler(message, ChannelSub)
    else:
        global CUR_REQ
        cut_link = message.text.split('/')[-1]
        if cut_link[0] == '+':
            CUR_REQ = {'order_type': 'sub', 'link': cut_link[1:], 'channel_type': 'private'}
        else:
            CUR_REQ = {'order_type': 'sub', 'link': cut_link, 'channel_type': 'public'}
        BOT.send_message(message.from_user.id, '❔ Введите желаемое количество подписок:')
        BOT.register_next_step_handler(message, SubscribersNumber)


def SubscribersNumber(message: telebot.types.Message) -> None:
    Stamp('Number inserting procedure', 'i')
    try:
        int(message.text)
        CUR_REQ['num'] = int(message.text)
        BOT.send_message(message.from_user.id, "❔ Введите промежуток времени (в минутах), "
                                               f"в течение которого будут происходить подписки:")
        BOT.register_next_step_handler(message, SubscriptionPeriod)
    except ValueError:
        BOT.send_message(message.chat.id, "❌ Пожалуйста, введите только число. Попробуйте ещё раз:")
        BOT.register_next_step_handler(message, SubscribersNumber)


def SubscriptionPeriod(message: telebot.types.Message) -> None:
    Stamp('Time inserting procedure', 'i')
    try:
        minutes = int(message.text)
        CUR_REQ['start'] = datetime.now()
        CUR_REQ['finish'] = datetime.now() + timedelta(minutes=minutes)
        REQS_QUEUE.append(CUR_REQ)
        BOT.send_message(message.from_user.id, "✅ Заявка принята. Начинаю выполнение подписок...")
    except ValueError:
        BOT.send_message(message.chat.id, "❌ Пожалуйста, введите только число. Попробуйте ещё раз:")
        BOT.register_next_step_handler(message, SubscriptionPeriod)


def SendActiveRequests(message: telebot.types.Message) -> None:
    if REQS_QUEUE:
        BOT.send_message(message.from_user.id, f' ✅Показываю {len(REQS_QUEUE)} активные заявки:')
        for req in REQS_QUEUE:
            BOT.send_message(message.from_user.id, f"*Начало*: {req['start'].strftime('%Y-%m-%d %H:%M')}\n"
                                                   f"*Конец*: {req['finish'].strftime('%Y-%m-%d %H:%M')}\n"
                                                   f"*Тип заказа*: {req['order_type']}\n"
                                                   f"*Желаемое количество*: {req['num']}\n"
                                                   f"*Выполненное количество*: {req.get('current_subs', 0)}\n"
                                                   f"*Ссылка*: {req['link']}\n"
                                                   f"*Тип канала*: {req['channel_type']}", parse_mode='Markdown')
    else:
        BOT.send_message(message.from_user.id, '🔍 Нет активных заявок')


@BOT.message_handler(content_types=['text'])
def MessageAccept(message: telebot.types.Message) -> None:
    Stamp(f'User {message.from_user.id} requested {message.text}', 'i')
    if message.text == '/start':
        BOT.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}!')
        ShowButtons(message, WELCOME_BTNS, '❔ Выберите действие:')
    elif message.text == WELCOME_BTNS[0]:
        BOT.send_message(message.from_user.id, '❔ Введите ссылку на канал (например, https://t.me/channel_name):')
        BOT.register_next_step_handler(message, ChannelSub)
    elif message.text == WELCOME_BTNS[1]:
        BOT.send_message(message.from_user.id, '❔ Отправьте пост, на котором необходимо увеличить просмотры:')
    elif message.text == WELCOME_BTNS[2]:
        SendActiveRequests(message)
        ShowButtons(message, WELCOME_BTNS, '❔ Выберите действие:')
    else:
        BOT.send_message(message.from_user.id, '❌ Я вас не понял...')
        ShowButtons(message, WELCOME_BTNS, '❔ Выберите действие:')


if __name__ == '__main__':
    Main()
