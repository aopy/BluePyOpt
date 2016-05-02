"""

"""

from .. import ephys


class PyNNSquarePulse(ephys.stimuli.Stimulus):

    def __init__(self, step_amplitude=None, step_delay=None,
                 step_duration=None, total_duration=None):
        super(PyNNSquarePulse, self).__init__()
        self.step_amplitude = step_amplitude
        self.step_delay = step_delay
        self.step_duration = step_duration
        self.total_duration = total_duration
        self.stim = None

    def instantiate(self, sim=None, icell=None):
        parameters = dict(amplitude=self.step_amplitude,
                          start=self.step_delay,
                          stop=self.step_delay + self.step_duration)
        if icell.electrode:
            icell.electrode.set_parameters(**parameters)
        else:
            icell.electrode = sim.sim.DCSource(**parameters)
            icell.electrode.inject_into(icell)

    def destroy(self):
        pass


class PyNNCurrentPlayStimulus(ephys.stimuli.Stimulus):

    def __init__(self, time_points, current_points, total_duration=None):
        super(PyNNCurrentPlayStimulus, self).__init__()
        self.time_points = time_points
        self.current_points = current_points
	self.total_duration = total_duration
        self.stim = None

    def instantiate(self, sim=None, icell=None):
        parameters = dict(amplitudes=self.current_points,
                          times=self.time_points)
        if icell.electrode:
            icell.electrode.set_parameters(**parameters)
        else:
            icell.electrode = sim.sim.StepCurrentSource(**parameters)
            icell.electrode.inject_into(icell)

    def destroy(self):
        pass

