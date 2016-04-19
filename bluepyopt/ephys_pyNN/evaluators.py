"""

"""


import logging
import numpy as np
from .. import ephys, optimisations


logger = logging.getLogger(__name__)


class PopulationEvaluator(ephys.evaluators.CellEvaluator):
    """
    """

    def __init__(
            self,
            cell_model=None,
            param_names=None,
            fitness_protocols=None,
            fitness_calculator=None,
            isolate_protocols=True,
            sim=None):

        self.cell_model = cell_model
        self.param_names = param_names
        # Stimuli used for fitness calculation
        self.fitness_protocols = fitness_protocols
        # Fitness value calculator
        self.fitness_calculator = fitness_calculator
        if isolate_protocols:
            logger.warning("PopulationEvaluator does not currently support protocol isolation")
        self.isolate_protocols = False
        self.sim = sim

    def param_dict(self, param_array):
        """Convert param_array in param_dict"""
        param_dict = {}
        param_array = np.array(param_array).transpose()
        for param_name, param_value in \
                zip(self.param_names, param_array):
            param_dict[param_name] = param_value

        return param_dict

    def evaluate_with_dicts(self, param_dict=None):
        """Run evaluation with dict as input and output"""

        if self.fitness_calculator is None:
            raise Exception(
                'PopulationEvaluator: need fitness_calculator to evaluate')

        responses = self.run_protocols(
            self.fitness_protocols.values(),
            param_dict)

        scores = []
        for channel in range(self.cell_model.size):
            # this part should perhaps be parallelised
            response = {}
            for label in responses:
                response[label] = responses[label][channel]
            scores.append(self.fitness_calculator.calculate_scores(response))
        return scores

    def evaluate_with_lists(self, param_list=None):
        """Run evaluation with lists as input and outputs

        `param_list` should be a list of lists, each sublist containing the parameters for one cell in the population
        """

        param_dict = self.param_dict(param_list)

        obj_dicts = self.evaluate_with_dicts(param_dict=param_dict)

        return [obj_dict.values() for obj_dict in obj_dicts]


# patch the bluepyopt.optimisations module

def evaluate_fitnesses(toolbox, individuals):
    # individuals is a list of lists, each list containing the parameters for one individual
    return toolbox.evaluate(individuals)

optimisations.evaluate_fitnesses = evaluate_fitnesses
