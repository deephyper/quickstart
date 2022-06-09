from deephyper.problem import HpProblem
from deephyper.evaluator import profile


hp_problem = HpProblem()
hp_problem.add_hyperparameter((-10.0, 10.0), "x")


@profile
def run(config):
    return -config["x"] ** 2


if __name__ == "__main__":
    import os
    import mpi4py
    from mpi4py import MPI
    import numpy as np

    from deephyper.evaluator import Evaluator
    from deephyper.search.hps import CBO
    from deephyper.evaluator.callback import ProfilingCallback, LoggingCallback

    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

    mpi4py.rc.initialize = False
    mpi4py.rc.threads = True
    mpi4py.rc.thread_level = "multiple"
    # mpi4py.rc.recv_mprobe = False

    if not MPI.Is_initialized():
        MPI.Init_thread()

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    timeout = None
    max_evals = 100
    random_state = 42

    rs = np.random.RandomState(random_state)
    rank_seed = rs.randint(low=0, high=2**32, size=size)[rank]

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
                random_state=rank_seed,
                log_dir="out",
            )

            # Executing the Search
            results = search.search(max_evals=max_evals)
