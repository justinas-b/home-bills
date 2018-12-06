class DateTranslator:

    _months = {
        "January": ["sausis", "sausio"],
        "February": ["vasaris", "vasario"],
        "March": ["kovas", "kovo"],
        "April": ["balandis", "balandzio"],
        "May": ["gegužė", "gegužės"],
        "June": ["birželis", "birželio"],
        "July": ["liepa", "liepos"],
        "August": ["rugpjūtis", "rugpjūčio"],
        "September": ["rugsėjis", "rugsėjo"],
        "October": ["spalis", "spalio"],
        "November": ["lapkritis", "lapkričio"],
        "December": ["gruodis", "gruodžio"],
    }

    @classmethod
    def translate_month_name(cls, month_name):
        name = [month for month in cls._months if month_name.casefold() in cls._months[month]]
        if not name:
            raise KeyError
        return name.pop()
