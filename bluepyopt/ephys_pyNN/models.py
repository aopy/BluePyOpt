"""

"""

import collections
from .. import ephys


class PyNNPopulationModel(ephys.models.CellModel):

    def __init__(self, name, size, celltype, params=None, initial_values=None):
        # each parameter is array-valued
        self.name = name
        self.size = size
        self.celltype = celltype
        self.params = collections.OrderedDict()
        for param in params:
            self.params[param.name] = param
        self.initial_values = initial_values
        self.icell = None
        self.instantiated = False

    def instantiate(self, sim=None):
        """Instantiate model in simulator"""
        parameters = dict((p.name, p.value) for p in self.params.values())
        parameters['v_spike'] = -40  # temporary hack; should set this elsewhere
        if self.instantiated:
            self.icell.set(**parameters)
        else:
            self.sim = sim.sim
            celltype = getattr(self.sim, self.celltype)
            self.icell = self.sim.Population(self.size, celltype, parameters,
                                            initial_values=self.initial_values,
                                            label=self.name)
            self.icell.record('spikes')
            self.icell.electrode = None
            self.instantiated = True

    def destroy(self):
        self.sim.reset()
