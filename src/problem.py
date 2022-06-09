from deephyper.problem import HpProblem
from deephyper.evaluator import profile


hp_problem = HpProblem()
hp_problem.add_hyperparameter((-10.0, 10.0), "x")

@profile
def run(config):
    return - config["x"]**2