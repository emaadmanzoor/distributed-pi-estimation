"""
    Client: Farms out workers to estimate Pi
    Args: None
    Returns: Sum of the circle_count's from
             all its workers
"""

import beanstalkc
import time

QUEUE_TO_USE = "msg_for_worker"
QUEUE_TO_WATCH = "msg_for_client"
QUEUE_TO_IGNORE = "default"

N = 10 ** 6                           # Number of darts to throw in total
K = 2                                 # Number of jobs to split the work into
TTR = 40                              # Deadline for jobs to complete (seconds)

beanstalk = beanstalkc.Connection(host="127.0.0.1", port=11300)

beanstalk.use(QUEUE_TO_USE)
beanstalk.watch(QUEUE_TO_WATCH)
beanstalk.ignore(QUEUE_TO_IGNORE)

use_queue_was_full = False
while True:                           # Block until the queue we push to is empty
    if (beanstalk.stats_tube(QUEUE_TO_USE)["current-jobs-ready"]
        + beanstalk.stats_tube(QUEUE_TO_USE)["current-jobs-reserved"]) == 0:
        break
    else:
        use_queue_was_full = True

start_time = time.time()

points_per_job = int(N / K)                   # Number of points per job
if not use_queue_was_full:
    for i in range(K):                            # Push all the jobs to the queue
        print "Put job", str(i), "to job queue"
        beanstalk.put(str(points_per_job), ttr=TTR)
    print

total_circle_count = 0
responses_received = 0
for i in range(K):
    job = beanstalk.reserve()
    responses_received += 1
    total_count = total_circle_count + int(job.body)
    job.delete()
    print "Received " + str(responses_received) + "/" + str(K) + " responses"
beanstalk.close()

pi = (4.0 * total_count) / (responses_received * points_per_job)

print
print "The value of pi is " + str(pi)
print "That took ", str(time.time() - start_time), " seconds!"
