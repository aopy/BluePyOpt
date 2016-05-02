"""

"""

from .. import ephys


class PyNNRecording(ephys.recordings.Recording):
    count = 0

    def __init__(self, name=None, value=None, frozen=None, variable='v', artificial_ap=30.0):
        super(PyNNRecording, self).__init__(name=name, value=value, frozen=frozen)
        self.variable = variable
        self.artificial_ap = artificial_ap

    def instantiate(self, sim=None, icell=None):
        """Instantiate recording"""
        self.population = icell
        self.sim = sim.sim
        if self.variable not in self.population.recorder.recorded:
            self.population.record(self.variable)
        self.instantiated = True
        self.index = self.__class__.count
        self.__class__.count += 1

    @property
    def response(self):
        """Return recording response"""
        if not self.instantiated:
            raise Exception(
                'Recording not instantiated before requesting response')
        data = self.population.get_data().segments[self.index]
        signal = data.filter(name=self.variable)[0]
        times = signal.times
        vm = signal.magnitude
        n_signals = vm.shape[1]
        if self.artificial_ap is not False:
            # add artificial action potentials at the time of each spike
            dt = self.sim.get_time_step()
            for i in range(n_signals):
                spike_times = data.spiketrains[i].magnitude
                if spike_times.size > 0:
                    spike_indices = (spike_times/dt).astype(int)
                    vm[spike_indices, i] = self.artificial_ap
        return [ephys.responses.TimeVoltageResponse(self.name, times, vm[:, i])
                for i in range(n_signals)]

    def destroy(self):
        pass
