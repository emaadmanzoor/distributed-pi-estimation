# Distributed Estimation of π

This system was built as a weekend assignment for the
Data Storage Technology and Networks course at 
[BITS - Pilani, KK Birla Goa Campus][1], under the guidance
of Dr. Biju K. R.

## Synopsis

   * We used [Beanstalkd][2] for our message queue.
   * We used [Beanstalkc][3] for Python bindings.
   * Our system is *fully worker-fault-tolerant*.
   * Our system is *partially server-fault-tolerant*.

## Contributors

   * Emaad Ahmed Manzoor
   * Rachee Singh

## Design And Implementation

A detailed description of the decision process and system design
is available on my [blog][4].

[1]: http://universe.bits-pilani.ac.in/Goa/ 
[2]: https://github.com/kr/beanstalkd
[3]: https://github.com/earl/beanstalkc
[4]: http://www.eyeshalfclosed.com/blog/2012/03/17/throwing-darts/

## See Also

[Distributed matrix multiplication with Beanstalkd](https://github.com/racheesingh/Beanstalkd-Cluster)
