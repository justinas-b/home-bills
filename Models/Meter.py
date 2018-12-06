class Meter:
    def __init__(self, previous_reading=0, current_reading=0, difference=None, units=None):
        self.current_reading = current_reading
        self.previous_reading = previous_reading
        self.units = units
        self.difference = difference

        if not difference:
            self.difference = self.current_reading - self.previous_reading

