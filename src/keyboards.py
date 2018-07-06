from telegram import *
from telegram.ext import Updater

multipliers = {'x1': 1, 'x2': 2, 'x3': 3, 'x4': 4, 'x5': 5, 'x10': 10}

no_games_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='Menu', callback_data='menu'),
                                         InlineKeyboardButton(text='Refresh', callback_data='game_list_refresh')]])


start_keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='Start game', callback_data='start_game'),
                                               InlineKeyboardButton(text='Available games', callback_data='game_list'),
                                               InlineKeyboardButton(text='Help', callback_data='help')]])

bet_keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='x1', callback_data="x1"),
                                             InlineKeyboardButton(text='x2', callback_data='x2'),
                                             InlineKeyboardButton(text='x3', callback_data='x3'),
                                             InlineKeyboardButton(text='x4', callback_data='x4'),
                                             InlineKeyboardButton(text='x5', callback_data='x5'),
                                             InlineKeyboardButton(text='x10', callback_data='x10'),
                                             InlineKeyboardButton(text='Time left: ', callback_data='time_left')]])

help_keyboard_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='<', callback_data='<'),
                                              InlineKeyboardButton(text='>', callback_data='>')]])



