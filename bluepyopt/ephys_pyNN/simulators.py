"""

"""

try:
    from importlib import import_module
except ImportError:  # Python 2.6
    def import_module(name):
        return __import__(name)


class PyNNSimulator(object):

    def __init__(self, simulator_engine):
        self.sim = import_module("pyNN.%s" % simulator_engine)
        self.sim.setup(verbosity='error')

    def run(self, tstop=None, cvode_active=True):
        """Run protocol"""
        self.sim.run(tstop)
