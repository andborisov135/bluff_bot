# -*- coding: utf-8 -*-
import random
import string
from typing import Optional
from game.bluffGame import BluffGame

__author__ = 'Rico'


# game_handler handles the Bluff-game-objects. When a new game is created, it is saved in the "game_list"
class GameHandler(object):
    class __GameHandler(object):
        def __init__(self):
            self.game_list = []  # List, where the running Games are stored in
            pass

        def gl_create(self) -> None:
            self.game_list = []

        def gl_remove(self, chat_id: int) -> None:
            index = self.get_index_by_chatid(chat_id)
            if index is None:
                return
            if not index < 0:
                self.game_list.pop(index)

        def get_index_by_chatid(self, chat_id: int) -> Optional[int]:
            for index, game in enumerate(self.game_list):
                if game.chat_id == chat_id:
                    return index
                else:
                    for player in game.players:
                        if player.user_id == chat_id:
                            return index

            return None

        def add_game(self, bluffgame: BluffGame) -> None:
            self.game_list.append(bluffgame)

        def get_game_by_chatid(self, chat_id: int) -> Optional[BluffGame]:
            index = self.get_index_by_chatid(chat_id)
            if index is None:
                return None
            return self.game_list[index]

        def get_game_by_index(self, index: int) -> BluffGame:
            return self.game_list[index]

        def get_game_by_id(self, game_id: int) -> Optional[BluffGame]:
            if game_id is None:
                return None
            for game in self.game_list:
                if game.game_id == game_id:
                    return game
            return None

        def generate_id(self) -> str:
            """Generates a random ID for a game"""
            game_id = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(8))

            while self.id_already_existing(game_id):
                print("ID already existing: " + str(game_id))
                game_id = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(8))

            return game_id

        def id_already_existing(self, game_id: str) -> bool:
            """Checks if an ID is already existing in the list of games"""
            for game in self.game_list:
                if game.game_id == game_id:
                    return True

            return False

        def get_game_by_user_id(self, user_id):
            for game in self.game_list:
                if game.player_one.user_id == user_id or game.player_two.user_id == user_id:
                    return game
            else:
                return None

        def get_game_id_by_user_id(self, user_id):
            return self.get_game_by_id(user_id).game_id


    instance = None

    def __init__(self):
        if not GameHandler.instance:
            GameHandler.instance = GameHandler.__GameHandler()

    @staticmethod
    def get_instance() -> __GameHandler:
        if not GameHandler.instance:
            GameHandler.instance = GameHandler.__GameHandler()

        return GameHandler.instance

