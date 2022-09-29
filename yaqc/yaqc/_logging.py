global logger



class NotLogger:

    def info(self, *args, **kwargs):
        ...




logger = NotLogger()
