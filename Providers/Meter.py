import inspect


class Meter:
    def __init__(self, provider=None, current_reading=None, previous_reading=None, difference=None):

        # TODO: Add price per meter

        if provider is not None:
            self.provider = provider
        else:
            self.provider = inspect.currentframe().f_back.f_locals['locals']['provider']

        self.current_reading = current_reading
        self.previous_reading = previous_reading

        if difference is None and previous_reading is not None:
            self.difference = current_reading - previous_reading
        else:
            self.difference = difference

