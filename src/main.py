from telegram.ext import CommandHandler, CallbackQueryHandler

from settings import *
from keyboards import *
from game.player import Player
from game.bluffGame import BluffGame
from datetime import datetime
from database.user_db import *

from gamehandler import GameHandler
game_handler = GameHandler.get_instance()

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# database things
Base.metadata.create_all()
Session = sessionmaker(bind=engine)
session = Session()

def start(bot, update):  # TODO display different messages for youser with 0 and non 0 blance
    eff_user = update.effective_user
    first_name = eff_user.first_name
    id = eff_user.id
    msg = 'Hello ' + str(first_name) + '!' + " Let's play!"
    #database
    if session.query(User.id).filter_by(id=id).scalar() is not None:
        update.message.reply_text(text=msg,
                                  reply_markup=start_keyboard_markup)
    else:
        update.message.reply_text(text=msg,
                                  reply_markup=start_keyboard_markup)
        u = User(name=first_name, id=id)
        session.add(u)
        session.commit()


def menu(bot, update):
    message_id = update.callback_query.message.message_id
    chat_id = update.effective_message.chat_id
    eff_user = update.effective_user
    first_name = eff_user.first_name
    msg = 'Hello ' + str(first_name) + '!' + " Let's play!"
    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text=msg,
                          reply_markup=start_keyboard_markup)


def start_game(bot, update, job_queue):
    message_id = update.callback_query.message.message_id
    chat_id = update.effective_message.chat_id
    eff_user = update.effective_user
    user_id = eff_user.id
    first_name = eff_user.first_name
    player = Player(user_id=user_id,
                    chat_id=chat_id,
                    message_id=message_id,
                    first_name=first_name,
                    bot=bot)

    game = BluffGame(game_id=game_handler.generate_id(),
                     created_player=player,
                     job_queue=job_queue,
                     turn_duration=20)
    game_handler.add_game(game)

    msg = "Awaiting your opponent"
    bot.edit_message_text(chat_id=player.chat_id,
                          message_id=player.message_id,
                          text=msg)


def list_games(bot, update):
    query = update.callback_query
    if game_handler.game_list == []:
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text='no game available',
                              reply_markup=no_games_markup)
    else:
        buttons = []
        for game in game_handler.game_list:
            buttons.append([InlineKeyboardButton(text=str(game.game_id), callback_data=str(game.game_id))])
        markup = InlineKeyboardMarkup(buttons)
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text='Chose the game',
                              reply_markup=markup)


def connect_game(bot, update):
    message = update.effective_message
    chat_id = message.chat_id
    eff_user = update.effective_user
    user_id = eff_user.id
    first_name = eff_user.first_name
    query_data = update.callback_query.data
    if game_handler.get_game_by_id(query_data) is not None:
        game = game_handler.get_game_by_id(query_data)
        player = Player(user_id=user_id,
                        chat_id=chat_id,
                        message_id=update.callback_query.message.message_id,
                        first_name=first_name,
                        bot=bot)
        game.join(player)
        game.start()


def make_bet(bot, update):
    query_data = update.callback_query.data
    multiplier = multipliers[query_data]
    eff_user = update.effective_user
    user_id = eff_user.id
    game = game_handler.get_game_by_user_id(user_id)

    # method returns flag if bet successfully multiplied
    flag = game.whose_turn.make_bet(100, multiplier)
    if flag and (game.awaiting_player.balance > 0):
        game.next_turn(bot, game.job)
    elif flag:
        game.stop()
        game_handler.game_list = []  # TODO proper removal
    else:
        if (game.whose_turn.balance <= 0) and (game.awaiting_player.balance <= 0):
            game.stop()
            game_handler.game_list = []  # TODO proper removal
        elif game.whose_turn.balance <= 0:
            game.next_turn(bot, game.job)
        else:
            msg = "Turn " + str(game.turn) + ' Fail! ' + 'Your turn ' + game.whose_turn.first_name + ' ' \
                  + 'Your balance: ' + str(game.whose_turn.balance) + ' Your bid: ' + str(game.whose_turn.bid)
            game.whose_turn.show_message(msg, bet_keyboard_markup)


def time_left(bot, update):
    query = update.callback_query
    eff_user = update.effective_user
    user_id = eff_user.id
    game = game_handler.get_game_by_user_id(user_id)
    time_elapsed = datetime.now() - game.turn_start
    turn_time_left = game.turn_duration - time_elapsed.seconds
    bot.answerCallbackQuery(callback_query_id=query.id,
                            text='Time left: ' + str(turn_time_left))


def help(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text='Game rules',
                          reply_markup=help_keyboard_markup)


def callback_eval(bot, update, job_queue):
    query_data = update.callback_query.data
    game_id_list = []
    for game in game_handler.game_list:
        game_id_list.append(game.game_id)

    if query_data == 'start_game':
        start_game(bot, update, job_queue)

    elif query_data == 'make_bet':
        make_bet(bot, update)

    elif query_data == 'game_list':
        list_games(bot, update)

    elif query_data == 'time_left':
        time_left(bot, update)

    elif query_data == 'help':
        help(bot, update)

    elif query_data == 'menu':
        menu(bot, update)

    elif query_data == 'game_list_refresh':
        list_games(bot, update)

    elif query_data in game_id_list:
        connect_game(bot, update)

    elif query_data in multipliers:
        make_bet(bot, update)


def main():
    """Run bot."""
    logging.debug('Main')
    start_handler = CommandHandler('start', start)
    callback_handler = CallbackQueryHandler(callback_eval,
                                            pass_job_queue=True)

    # adding handlers
    handlers = [start_handler,
                callback_handler]

    for handler in handlers:
        dispatcher.add_handler(handler)

    updater.start_webhook(listen='0.0.0.0', port=8000, url_path=TOKEN)  # webhook_url=(URL + TOKEN)
    updater.bot.set_webhook(URL + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()