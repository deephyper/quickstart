from deephyper.problem import HpProblem
from deephyper.evaluator import profile


hp_problem = HpProblem()
hp_problem.add_hyperparameter((-10.0, 10.0), "x")


@profile
def run(config):
    return -config["x"] ** 2


if __name__ == "__main__":
    import os

    from deephyper.evaluator import Evaluator
    from deephyper.search.hps import CBO
    from deephyper.evaluator.callback import ProfilingCallback, LoggingCallback

    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

    timeout = 10*60 # in seconds
    max_evals = None
    random_state = 42
    log_dir = "out"

    profiler = ProfilingCallback()
    logger = LoggingCallback()

    # Creating the Evaluator
    with Evaluator.create(
        run,
        method="mpicomm",
        method_kwargs={
            "callbacks": [profiler, logger],
        },
    ) as evaluator:
        if evaluator is not None:

            # Creating the Search
            search = CBO(
                hp_problem,
                evaluator,
                multi_point_strategy="qUCB",
                random_state=random_state,
                log_dir=log_dir,
            )

            # Executing the Search
            results = search.search(timeout=timeout)
