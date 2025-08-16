class State:
    """ state handles game state """

    def __init__(self, data=None):
        self._data = data or {}
        self._end_started = 0
        self._images_shown = 0
        self._explosion = None
        self._fired = False
        self._wait = 0
        self._game_over_wait = 0
        self._game_over_done = False
        self._last_x = 0
        self._last = 0
        self._difference = 0

    @property
    def end_started(self):
        """get end_started"""
        return self._end_started

    @end_started.setter
    def end_started(self, value):
        """set end_started"""
        self._end_started = value

    @property
    def images_shown(self):
        """get images shown"""
        return self._images_shown

    @images_shown.setter
    def images_shown(self, value):
        """set images_shown"""
        self._images_shown = value

    @property
    def explosion(self):
        """get explosion"""
        return self._explosion

    @explosion.setter
    def explosion(self, value):
        """set explosion"""
        self._explosion = value

    @property
    def fired(self):
        """get fired"""
        return self._fired

    @fired.setter
    def fired(self, value):
        """set fired"""
        self._fired = value

    @property
    def wait(self):
        """get wait"""
        return self._wait

    @wait.setter
    def wait(self, value):
        """set wait"""
        self._wait = value

    @property
    def game_over_wait(self):
        """set game over wait"""
        return self._game_over_wait

    @game_over_wait.setter
    def game_over_wait(self, value):
        """set game_over_wait"""
        self._game_over_wait = value

    @property
    def game_over_down(self):
        """set game over wait"""
        return self._game_over_down

    @game_over_down.setter
    def game_over_down(self, value):
        """set game_over_wait"""
        self._game_over_down = value

    @property
    def last_x(self):
        """get last x"""
        return self._last_x

    @last_x.setter
    def last_x(self, value):
        """set last_x"""
        self._last_x = value

    @property
    def last(self):
        """get last"""
        return self._last

    @last.setter
    def last(self, value):
        """set last"""
        self._last = value

    @property
    def difference(self):
        """get difference"""
        return self._difference

    @difference.setter
    def difference(self, value):
        """set differebce"""
        self._difference = value

    def update(self, key, value):
        """update dynamic value"""
        self._data[key] = value

    def get(self, key, default=None):
        """get dynamic value"""
        return self._data.get(key, default)
