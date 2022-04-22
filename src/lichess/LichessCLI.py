import logging
from conf import settings

from ChallengeStreamWatcher import ChallengeStreamWatcher
from EventStreamWatcher import EventStreamWatcher
from GameManager import GameManager

# TODO: Maybe make this an enum?
MENU_OPTIONS = {
    1: "Automatic matchmaking",
    2: "Challenge the AI",
    3: "Challenge a user",
    4: "Help",
    5: "Quit"
}

class LichessCLI:
    def __init__(self, lichess_api, game_manager, challenge_stream_watcher, event_stream_watcher, threads):
        self.is_running = True
        self.api = lichess_api
        self.game_manager = game_manager
        self.challenge_stream_watcher = challenge_stream_watcher
        self.event_stream_watcher = event_stream_watcher

    def run(self):
        print("Welcome to the Lichess CLI tool. Please select one of the commands below: ")
        self._print_menu()

        while self.is_running:
            command = int(input("Enter your choice: "))

            if (command == 1):
                self._matchmaking()
            elif (command == 2):
                self._challenge_ai()
            elif (command == 3):
                user = input("Enter a username: ")
                self._challenge_user(user)
            elif (command == 4):
                self._print_menu()
            elif (command == 5):
                '''
                TODO:
                1) Detect Ctrl-C and route it to this option
                2) Gracefully shut down all threads and release their memory
                '''
                self._quit()
            else:
                print("Sorry, I don't understand that command. Please try again.")

    def _print_menu(self):
        for key in MENU_OPTIONS.keys():
            print(f"{key}. -- {MENU_OPTIONS[key]}")

    def _matchmaking(self):
        # TODO: Turn on or off matchmaking
        return 0

    def _challenge_ai(self):
        return 0

    def _challenge_user(self, username):
        self.challenge_stream_watcher.challenge_user(username)
        
    def _quit(self):
        if self.game_manager.do_games_exist():
            print("Sorry, there's still games currently running. This will close once the games finish...")
        self._close_all_threads()
        self.is_running = False

    def _close_all_threads(self):
        # for thread in self.threads:
        #     thread.stop()
        
        # for thread in self.threads:
        #     thread.wait()
        #     # TODO: self.threads.pop()
        return 0