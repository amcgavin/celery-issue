import time

from celery import Celery

app = Celery("tasks", broker="pyamqp://guest@broker//")


class BrokenException(Exception):
    """
    This Exception can't be unpickled by default
    """
    def __init__(self, msg, other_arg):
        super().__init__(msg)
        self.other_arg = other_arg


@app.task
def regular_task():
    return "done"


@app.task
def safe_exception():
    """
    This task won't crash the process, but will still raise an exception in the task handler.
    """
    raise BrokenException("msg", "other_arg")


@app.task(bind=True)
def unsafe_exception(self):
    """
    This task will crash the worker process.
    """
    self.retry(exc=BrokenException("msg", "other_arg"))


def main():
    safe_exception.delay()
    time.sleep(1)
    regular_task.delay()
    time.sleep(1)
    unsafe_exception.delay()
    time.sleep(1)
    regular_task.delay()


if __name__ == "__main__":
    main()
