from datetime import datetime
from telegram import *


whose_turn_message = "Turn #{turn}. Your turn {name}. Your balance: {balance}. Your bid: {bid}"
whose_turn_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='x1', callback_data="x1"),
                                             InlineKeyboardButton(text='x2', callback_data='x2'),
                                             InlineKeyboardButton(text='x3', callback_data='x3'),
                                             InlineKeyboardButton(text='x4', callback_data='x4'),
                                             InlineKeyboardButton(text='x5', callback_data='x5'),
                                             InlineKeyboardButton(text='x10', callback_data='x10'),
                                             InlineKeyboardButton(text='Time left: ', callback_data='time_left')]])
awaiting_player_message = "Turn #{turn}. {name}, wait until your turn. Your balance: {balance}. Your bid: {bid}."
awaiting_player_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='Time left: ', callback_data='time_left')]])
back_to_menu_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='Menu', callback_data='menu')]])

class BluffGame(object):
    def __init__(self,
                 game_id,
                 job_queue,
                 created_player,
                 turn_duration=7):  # turn_duration in sec
        self.game_id = game_id
        self.job_queue = job_queue
        self.job = None
        self.turn_duration = turn_duration # in sec
        self.turn_start = None
        self.turn = 1
        self.whose_turn = created_player
        self.player_one = created_player
        self.player_two = None
        self.awaiting_player = self.player_two

    def join(self, player):
        self.player_two = player
        self.awaiting_player = self.player_two

    def start(self):
        self.initiate_turn_timer()
        self.whose_turn.show_message(whose_turn_message.format(turn=self.turn,
                                                               name=self.whose_turn.first_name,
                                                               balance=self.whose_turn.balance,
                                                               bid=self.whose_turn.bid),
                                     whose_turn_markup)
        self.awaiting_player.show_message(awaiting_player_message.format(turn=self.turn,
                                                                         name=self.awaiting_player.first_name,
                                                                         balance=self.awaiting_player.balance,
                                                                         bid=self.whose_turn.bid),
                                          awaiting_player_markup)

    def next_turn(self, bot, job):
        self.switch_player()
        self.job.schedule_removal()
        self.turn += 1
        self.initiate_turn_timer()
        self.whose_turn.show_message(whose_turn_message.format(turn=self.turn,
                                                               name=self.whose_turn.first_name,
                                                               balance=self.whose_turn.balance,
                                                               bid=self.whose_turn.bid),
                                     whose_turn_markup)

        self.awaiting_player.show_message(awaiting_player_message.format(turn=self.turn,
                                                                         name=self.awaiting_player.first_name,
                                                                         balance=self.awaiting_player.balance,
                                                                         bid=self.awaiting_player.bid),
                                          awaiting_player_markup)

    def initiate_turn_timer(self):
        self.turn_start = datetime.now()
        self.job = self.job_queue.run_once(self.next_turn,
                                           self.turn_duration)

    def switch_player(self):
        if self.whose_turn == self.player_one:
            self.whose_turn = self.player_two
            self.awaiting_player = self.player_one
        else:
            self.whose_turn = self.player_one
            self.awaiting_player = self.player_two

    def stop(self):
        print("game.stop()")
        self.job.schedule_removal()
        print(1)
        winner_msg = "You Won! Congrats! Your bid {win_bid}. Your opponents bid {lose_bid}."
        looser_msg = "You Lose! Your bid {lose_bid}. Your opponents bid {win_bid}."
        print(self.player_one.bid > self.player_two.bid)
        if self.player_one.bid > self.player_two.bid:
            print(2)
            winner_msg = winner_msg.format(win_bid=self.player_one.bid, lose_bid=self.player_two.bid)
            looser_msg = looser_msg.format(win_bid=self.player_one.bid, lose_bid=self.player_two.bid)
            self.player_one.show_message(winner_msg, back_to_menu_markup)
            self.player_two.show_message(looser_msg, back_to_menu_markup)
            print(3)
        elif self.player_two.bid > self.player_one.bid:
            print(4)
            winner_msg = winner_msg.format(win_bid=self.player_two.bid, lose_bid=self.player_one.bid)
            looser_msg = looser_msg.format(win_bid=self.player_two.bid, lose_bid=self.player_one.bid)
            self.player_one.show_message(looser_msg, back_to_menu_markup)
            self.player_two.show_message(winner_msg, back_to_menu_markup)
            print(5)
        else:
            print('Tie else')
            msg = 'A Tie! {p_one_name} bid is {p_one_bid}, {p_two_name} bid is {p_two_bid}'
            msg = msg.format(p_one_name=self.player_one.first_name,
                             p_two_name=self.player_two.first_name,
                             p_one_bid=self.player_one.bid,
                             p_two_bid=self.player_two.bid)
            print('ok')
            self.player_one.show_message(msg, back_to_menu_markup)
            self.player_two.show_message(msg, back_to_menu_markup)