import talib


class IndicatorMeta(type):

    def __new__(cls, name, bases, attrs):
        instance = type.__new__(cls, name, bases, attrs)

        for func in talib.get_functions():
            setattr(instance, func, instance.retrieve) #getattr(talib, func))

        return instance

    def __getattr__(cls, func):
        def do_init(data, **kwargs):
            return Indicator(func, data, **kwargs)

        return do_init


class Indicator(metaclass=IndicatorMeta):

    def __init__(self, func, data, **kwargs):
        self.func = talib.abstract.Function(func)
        self.func.parameters = kwargs

        self.out_lines = len(self.func.output_names)
        self.lookback = self.func.lookback

    def __call__(self, data, **kwargs):
        # return on __init__ call from strategy where data is passed as `None` or `[]`
        if not any(data):
            return self

        self.lines = self.func({ 'close': data }, **kwargs)
        return self

    def get_lines(self):
        # Returns list of lines, wrap in a list if number of lines < 1
        return self.lines if self.out_lines > 1 else [self.lines]
