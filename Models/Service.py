class Service:
    def __init__(self, name=None, bill=None, meter=None):
        self.name = name
        self.bill = bill
        self.meter = meter
        self.has_meter = False

        if meter:
            self.has_meter = True
