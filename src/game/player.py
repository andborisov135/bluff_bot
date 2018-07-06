from numpy.random import choice


class Player(object):
    def __init__(self, user_id, chat_id, message_id, first_name, bot, balance=100):
        self.user_id = user_id
        self.chat_id = chat_id
        self.message_id = message_id
        self.first_name = first_name
        self.bot = bot
        self.balance = balance
        self.bid = 0

    def make_bet(self, bet, multiplication, penalty=1):
        print('making bet')
        probability = 1 / multiplication
        outcome = choice([0, 1], 1, p=[1 - probability, probability])
        if outcome == 1:
            self.balance = self.balance - bet
            self.bid += bet*multiplication
            return True
        else:
            self.balance = self.balance - (penalty * bet)
            return False

    def show_message(self, message, markup):
        self.bot.edit_message_text(chat_id=self.chat_id,
                                   message_id=self.message_id,
                                   text=message,
                                   reply_markup=markup)