from timeit import default_timer as timer

class Timer(object):
    def __enter__(self):
        self.start = timer()

    def __exit__(self, *args):
        self.end = timer()
        self.duration = self.end - self.start
        print('Timer:', self.duration)
