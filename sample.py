import random
import sys

class Sample(object):
    def __init__(self, sample_size):
        self._sample_size = sample_size
        self._samples = []
        self._flow_cnt = 0

    def add(self, s):
        self._flow_cnt += 1
        if self._flow_cnt <= self._sample_size:
            self._samples.append(s)
        else:
            r = random.randint(1, self._flow_cnt)
            if r <= self._sample_size:
                r = random.randint(1, self._sample_size)
                #print "1\t%s" % self._samples[r - 1],
                self._samples[r - 1] = s
            else:
                pass
                #print "1\t%s" % s,
        return self

    def sampling(self):
        for i in self._samples:
            yield i
        #return self._samples

    def oversampling(self):
        for i in self._samples:
            yield i
        _len = len(self._samples)
        _len_i = _len
        while(_len_i < self._sample_size):
            r = random.randint(1, _len)
            yield self._samples[r-1]
            _len_i += 1


if __name__ == "__main__":
    sampler = Sample(int(sys.argv[1]))
    is_oversampling = sys.argv[2]
    if len(sys.argv) != 3:
        print >>sys.stderr, "python sample.py sample_num True/False"
        sys.exit(-1)

    for line in sys.stdin:
        sampler.add(line)

    if is_oversampling == "False":
        for i in  sampler.sampling():
            print i,
    else:
        for i in  sampler.oversampling():
            print i,
