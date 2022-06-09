import logging
import pathlib
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import mpi4py

mpi4py.rc.initialize = False
mpi4py.rc.threads = True
mpi4py.rc.thread_level = "multiple"
# mpi4py.rc.recv_mprobe = False

import numpy as np

from deephyper.evaluator import Evaluator
from deephyper.search.hps import CBO
from deephyper.evaluator.callback import ProfilingCallback

from mpi4py import MPI

if not MPI.Is_initialized():
    MPI.Init_thread()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

from .problem import hp_problem, run


def execute(
    sync,
    timeout,
    random_state,
    log_dir,
    n_jobs,
    model,
):
    """Execute the CBO algorithm.
    Args:
        sync (bool): Boolean to execute the search in "synchronous" (``True``) or "asynchronous" (``False``) communication.
        timeout (int): duration in seconds of the search.
        random_state (int): random state/seed of the search.
        log_dir (str): path of the logging directory (i.e., where to store results).
        max_evals (int): maximum number of evaluations for the search.
    """
    rs = np.random.RandomState(random_state)
    rank_seed = rs.randint(low=0, high=2**32, size=size)[rank]

    log_dir = log_dir
    pathlib.Path(log_dir).mkdir(parents=False, exist_ok=True)

    if rank == 0:
        path_log_file = os.path.join(log_dir, "deephyper.log")
        logging.basicConfig(
            filename=path_log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s - %(message)s",
            force=True,
        )

        # Evaluator creation
        logging.info("Creation of the Evaluator...")

    profiler = ProfilingCallback()

    with Evaluator.create(
        run,
        method="mpicomm",
        method_kwargs={
            "callbacks": [profiler],
        },
    ) as evaluator:
        if evaluator is not None:
            logging.info(
                f"Creation of the Evaluator done with {evaluator.num_workers} worker(s)"
            )

            # Search
            logging.info("Creation of the search instance...")
            search = CBO(
                hp_problem,
                evaluator,
                sync_communication=sync,
                multi_point_strategy="qUCB",
                n_jobs=n_jobs,
                log_dir=log_dir,
                random_state=rank_seed,
                acq_func="UCB",
                surrogate_model=model,
            )
            logging.info("Creation of the search done")

            logging.info("Starting the search...")
            results = search.search(timeout=timeout)
            logging.info("Search is done")

            results.to_csv(os.path.join(log_dir, f"results.csv"))
