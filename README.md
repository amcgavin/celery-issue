## Celery bug example

Passing an Exception that cannot be pickled and unpickled crashes celery worker processes.

## Running

This example uses Docker and docker-compose. Instructions will not be provided on setting these up.

1. Build the container with `docker-compose build celery`
2. Start the containers with `docker-compose up -d celery`
3. Queue up the test tasks with `docker-compose run --rm celery python tasks.py`
4. Check logs with `docker-compose logs celery`

```
celery_1  | [2021-10-08 08:34:08,175: ERROR/ForkPoolWorker-2] Task tasks.safe_exception[27750f2e-dc7c-410f-83f6-d9b77dd95583] raised unexpected: BrokenException('msg')
celery_1  | Traceback (most recent call last):
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/app/trace.py", line 450, in trace_task
celery_1  |     R = retval = fun(*args, **kwargs)
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/app/trace.py", line 731, in __protected_call__
celery_1  |     return self.run(*args, **kwargs)
celery_1  |   File "/app/code/tasks.py", line 27, in safe_exception
celery_1  |     raise BrokenException("msg", "other_arg")
celery_1  | tasks.BrokenException: msg
celery_1  | [2021-10-08 08:34:08,177: ERROR/MainProcess] Task handler raised error: <MaybeEncodingError: Error sending result: '"(1, <ExceptionInfo: BrokenException('msg')>, None)"'. Reason: ''PicklingError("Can\'t pickle <class \'tasks.BrokenException\'>: it\'s not the same object as tasks.BrokenException")''.>
celery_1  | Traceback (most recent call last):
celery_1  |   File "/usr/local/lib/python3.7/site-packages/billiard/pool.py", line 366, in workloop
celery_1  |     put((READY, (job, i, result, inqW_fd)))
celery_1  |   File "/usr/local/lib/python3.7/site-packages/billiard/queues.py", line 366, in put
celery_1  |     self.send_payload(ForkingPickler.dumps(obj))
celery_1  |   File "/usr/local/lib/python3.7/site-packages/billiard/reduction.py", line 56, in dumps
celery_1  |     cls(buf, protocol).dump(obj)
celery_1  | billiard.pool.MaybeEncodingError: Error sending result: '"(1, <ExceptionInfo: BrokenException('msg')>, None)"'. Reason: ''PicklingError("Can\'t pickle <class \'tasks.BrokenException\'>: it\'s not the same object as tasks.BrokenException")''.
celery_1  | [2021-10-08 08:34:09,176: INFO/MainProcess] Task tasks.regular_task[662b30a3-825e-4a26-ba23-33e8011d7dad] received
celery_1  | [2021-10-08 08:34:09,177: INFO/ForkPoolWorker-2] Task tasks.regular_task[662b30a3-825e-4a26-ba23-33e8011d7dad] succeeded in 0.0001365000061923638s: 'done'
celery_1  | [2021-10-08 08:34:10,180: INFO/MainProcess] Task tasks.unsafe_exception[38b08c18-451b-4645-a4ac-ada2e6b43e5e] received
celery_1  | [2021-10-08 08:34:10,200: INFO/ForkPoolWorker-2] Task tasks.unsafe_exception[38b08c18-451b-4645-a4ac-ada2e6b43e5e] retry: Retry in 180s: BrokenException('msg')
celery_1  | [2021-10-08 08:34:10,200: INFO/MainProcess] Task tasks.unsafe_exception[38b08c18-451b-4645-a4ac-ada2e6b43e5e] received
celery_1  | [2021-10-08 08:34:10,201: CRITICAL/MainProcess] Unrecoverable error: TypeError("__init__() missing 1 required positional argument: 'other_arg'")
celery_1  | Traceback (most recent call last):
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/worker/worker.py", line 203, in start
celery_1  |     self.blueprint.start(self)
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/bootsteps.py", line 116, in start
celery_1  |     step.start(parent)
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/bootsteps.py", line 365, in start
celery_1  |     return self.obj.start()
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/worker/consumer/consumer.py", line 326, in start
celery_1  |     blueprint.start(self)
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/bootsteps.py", line 116, in start
celery_1  |     step.start(parent)
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/worker/consumer/consumer.py", line 618, in start
celery_1  |     c.loop(*c.loop_args())
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/worker/loops.py", line 81, in asynloop
celery_1  |     next(loop)
celery_1  |   File "/usr/local/lib/python3.7/site-packages/kombu/asynchronous/hub.py", line 361, in create_loop
celery_1  |     cb(*cbargs)
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/concurrency/asynpool.py", line 325, in on_result_readable
celery_1  |     next(it)
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/concurrency/asynpool.py", line 306, in _recv_message
celery_1  |     message = load(bufv)
celery_1  | TypeError: __init__() missing 1 required positional argument: 'other_arg'
celery_1  | [2021-10-08 08:34:41,378: ERROR/MainProcess] Task handler raised error: WorkerLostError('Worker exited prematurely: exitcode 0 Job: 2.')
celery_1  | Traceback (most recent call last):
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/worker/worker.py", line 203, in start
celery_1  |     self.blueprint.start(self)
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/bootsteps.py", line 116, in start
celery_1  |     step.start(parent)
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/bootsteps.py", line 365, in start
celery_1  |     return self.obj.start()
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/worker/consumer/consumer.py", line 326, in start
celery_1  |     blueprint.start(self)
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/bootsteps.py", line 116, in start
celery_1  |     step.start(parent)
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/worker/consumer/consumer.py", line 618, in start
celery_1  |     c.loop(*c.loop_args())
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/worker/loops.py", line 81, in asynloop
celery_1  |     next(loop)
celery_1  |   File "/usr/local/lib/python3.7/site-packages/kombu/asynchronous/hub.py", line 361, in create_loop
celery_1  |     cb(*cbargs)
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/concurrency/asynpool.py", line 325, in on_result_readable
celery_1  |     next(it)
celery_1  |   File "/usr/local/lib/python3.7/site-packages/celery/concurrency/asynpool.py", line 306, in _recv_message
celery_1  |     message = load(bufv)
celery_1  | TypeError: __init__() missing 1 required positional argument: 'other_arg'
celery_1  | 
celery_1  | During handling of the above exception, another exception occurred:
celery_1  | 
celery_1  | Traceback (most recent call last):
celery_1  |   File "/usr/local/lib/python3.7/site-packages/billiard/pool.py", line 1267, in mark_as_worker_lost
celery_1  |     human_status(exitcode), job._job),
celery_1  | billiard.exceptions.WorkerLostError: Worker exited prematurely: exitcode 0 Job: 2.
celery-example_celery_1 exited with code 0
```
