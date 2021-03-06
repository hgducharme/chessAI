import json
import logging
from conf import settings
from ContinuousWorker import ContinuousWorker

logger = logging.getLogger(__name__)

class ChallengeStreamWatcher(ContinuousWorker):
    def __init__(self, lichess_api, game_manager, *args, **kwargs):
        logger.debug(logger.name)
        super().__init__(*args, **kwargs)
        self.api = lichess_api
        self.game_manager = game_manager
        self.username_queue = []

    def work(self):
        if self.game_manager.number_of_games() == settings.MAX_NUMBER_OF_GAMES:
            return

        self._send_user_challenge()
        self._do_automatic_matchmaking()

    def challenge_user(self, username = None):
        self.username_queue.append(username)

    def _send_user_challenge(self):
        if len(self.username_queue) > 0:
            username = self.username_queue.pop(0)
            logger.info(f"Sending a challenege request to user {username}")
            response = self.api.create_challenge(username, settings.CHALLENGE_PARAMS["real_time"])
            logger.info(f"Response from challenge request to {username}: {response}")

    def _do_automatic_matchmaking(self):
        if settings.AUTO_MATCHMAKING == True:
            challenges_stream = self.api.stream_challenges()
            self.challenges = self._parse_stream(challenges_stream)
            if self._challenges_exist():
                self._accept_challenge()
            else:
                self._send_bot_challenge()

    def _parse_stream(self, stream):
        items_in_stream = []
        for line in stream:
            if line:
                line = json.loads(line)
                items_in_stream.append(line)

        if (len(items_in_stream) == 1):
            return items_in_stream[0]

        return tuple(items_in_stream)

    def _challenges_exist(self):
        incoming_challenges = self.challenges["in"]
        return (len(incoming_challenges) > 0)

    def _accept_challenge(self):
        return 0

    def _send_bot_challenge(self):
        online_bots = self.api.stream_online_bots()
        online_bots = self._parse_stream(online_bots)

    def _cleanup(self):
        # TODO: Cleanup resources
        return