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
        ## parameters['v_spike'] = -40  # temporary hack; should set this elsewhere
        if self.instantiated:
            self.icell.set(**parameters)
        else:
            celltype = getattr(sim.sim, self.celltype)
            self.icell = sim.sim.Population(self.size, celltype, parameters,
                                            initial_values=self.initial_values,
                                            label=self.name)
            self.icell.record('spikes')
            self.icell.electrode = None
            self.instantiated = True

    def destroy(self, sim=None):
        sim.sim.reset()

    def __str__(self):
        """Return string representation"""

        content = '%s:\n' % self.name

        content += '  cell type:\n'
        if self.celltype is not None:
            content += '    %s\n' % self.celltype

        content += '  params:\n'
        if self.params is not None:
            for param in self.params.values():
                content += '    %s\n' % param

        return content