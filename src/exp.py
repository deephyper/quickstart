import argparse
import pathlib
import sys

from .search import execute

def create_parser():
    parser = argparse.ArgumentParser(description="Command line to run experiments.")

    parser.add_argument(
        "--model",
        type=str,
        choices=["RF", "GP", "DUMMY"],
        required=False,
        default="RF",
        help="Surrogate model used by the Bayesian optimizer.",
    )
    parser.add_argument(
        "--sync",
        type=int,
        default=0,
        help="If the search workers must be syncronized or not.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Search maximum duration (in min.) for each optimization.",
    )
    parser.add_argument(
        "--max-evals",
        type=int,
        default=-1,
        help="Number of iterations to run for each optimization.",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Control the random-state of the algorithm.",
    )
    parser.add_argument(
        "--log-dir",
        type=str,
        default="output",
        help="Logging directory to store produced outputs.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        type=bool,
        default=False,
        help="Wether to activate or not the verbose mode.",
    )
    parser.add_argument(
        "--n-jobs",
        type=int,
        default=4,
        help="The number of parallel processes to use to fit the surrogate model.",
    )

    return parser


def main(args):

    sync = bool(args.sync)

    pathlib.Path(args.log_dir).mkdir(parents=True, exist_ok=True)

    execute(
        sync,
        args.timeout,
        args.random_state,
        args.log_dir,
        args.n_jobs,
        args.model,
    )


if __name__ == "__main__":
    parser = create_parser()

    args = parser.parse_args()

    # delete arguments to avoid conflicts
    sys.argv = [sys.argv[0]]

    main(args)