"""
    Worker: Performs Monte-Carlo estimation of Pi
    Receives: n, the number of darts to throw
    Returns: c, the number of darts lying withing the circle
"""

import beanstalkc
import random
import time

QUEUE_TO_WATCH = "msg_for_worker"
QUEUE_TO_USE = "msg_for_client"
QUEUE_TO_IGNORE = "default"

while True:                             # Indefinitely wait for jobs to do

    print "Connecting to job server..."
    beanstalk = beanstalkc.Connection(host='127.0.0.1', port=11300)

    beanstalk.watch(QUEUE_TO_WATCH)     # Reserve jobs from this queue
    beanstalk.ignore(QUEUE_TO_IGNORE)   # Ignore this queue for reservation

    print "Waiting for jobs..."
    job = beanstalk.reserve()           # Blocks until a job is available

    n = int(job.body)                   # n = number of darts to throw
    start_time = time.time()

    # Algorithm Reference: Monte-Carlo estimation of Pi
    # Source: https://computing.llnl.gov/tutorials/parallel_comp/#ExamplesPI

    square_edge = 2.0                    # Square edge length
    center_x, center_y = 1.0, 1.0        # Circle center coordinates
    radius = 1.0                         # Circle radius
    circle_count = 0                     # Counts points within the circle

    print
    print "Generating", str(n), "points..."
    try:
        for i in xrange(n):
            x = random.random() * square_edge        # 0 <= x < square_edge
            y = random.random() * square_edge        # 0 <= y < square_edge
            if (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2:
                circle_count = circle_count + 1
    except Exception:
        print "Job failed.", n
        job.release()

    beanstalk.use(QUEUE_TO_USE)         # Push the calculated number of points
    beanstalk.put(str(circle_count))    # in the circle to the client queue

    job.delete()                        # Tell the job server you're done
    beanstalk.close()

    print "Finished job in", str(time.time() - start_time), "seconds"
    print
