"""
Hop along fun.

29/08/2025.
"""

from __future__ import annotations

from typing import Optional

import matplotlib
import matplotlib.pyplot as plt
import numba as nb
import numpy as np
import numpy.typing as npt


DEBUG = False


@nb.njit(debug=DEBUG)
def hop_along_eq(xy: npt.NDArray, a: float, b: float, c: float) -> npt.NDArray:
    """
    Complete 1 iteration of the hop along equation.

    Used https://www.jolinton.co.uk/Mathematics/Hopalong_Fractals/Text.pdf
    as a reference.

    x' = y + f(x) where f(x) = -SGN(x)*sqrt(|bx-c|)
    y' = a - x

    Args:
        xy (npt.NDArray): Initial coordiates to iterate on.
        a (float): Hop along parameter.
        b (float): Hop along parameter.
        c (float): Hop along parameter.

    Returns:
        npt.NDArray: The resulting coordinate from the iteration.
    """
    sqrt_x = np.sqrt(np.abs(b * xy[0] - c))

    f_x = -np.copysign(sqrt_x, xy[0])  # Classic BM
    # f_x = +np.copysign(sqrt_x, xy[0]) # Positive BM, also cool
    # f_x = sqrt_x # Additive, not bad
    # f_x = np.sin(b*xy[0] - c) # Sinusoidal, pretty interesting
    # f_x = np.abs(b*xy[0]) # Gingerbread Man, kinda meh

    new_x = xy[1] + f_x
    new_y = a - xy[0]
    return np.array([new_x, new_y])


@nb.njit(debug=DEBUG)
def hop_along_for_n(
    a: float,
    b: float,
    c: float,
    n_iters: int,
    xy_init: Optional[npt.NDArray] = None,
) -> npt.NDArray:
    """
    Calculate `n_iters` iterations of the hop along equations for parameters (a,b,c).

    Use this function to generate a sample of iterations for a set of parameters.
    By default, this function uses (0,0) for initial conditions, but this can be
    overridden by setting `xy_init`.

    Args:
        a (float):
            Hop along parameter.
        b (float):
            Hop along parameter.
        c (float):
            Hop along parameter.
        n_iters (int):
            Number of iterations to calculate.
        xy_init (NDArray, optional):
            Initial conditions for the iteration. Defaults to (0,0).

    Returns:
        npt.NDArray: The results of each iteration with shape (n_iters, 2).
    """
    ret = np.zeros((n_iters, 2))

    if xy_init is None:
        xy_init = np.array([0.0, 0.0])
    xy = xy_init
    for index in range(n_iters):
        xy = hop_along_eq(xy, a, b, c)
        ret[index, 0] = xy[0]
        ret[index, 1] = xy[1]
    return ret


def random_abc(
    min_val: float = -10.0,
    max_val: float = +10.0,
) -> tuple[float, float, float]:
    """
    Generate a random set of parameters.

    Args:
        min_val (float, optional):
            The smallest value any of the parameters can take. Defaults to -10.0.
        max_val (float, optional):
            The largest value any of the parameters can take. Defaults to +10.0.

    Returns:
        tuple[float, float, float]: The generated parameters.
    """
    return tuple(np.random.uniform(min_val, max_val) for _ in range(3))  # type: ignore


def plot_hop_along(
    a: float,
    b: float,
    c: float,
    n_iters: int,
    *,
    n_hist: int,
    n_reset: int,
    alpha_init: float = 0.3,
    pause_time: float = 0.9,
) -> None:
    """
    Opens a matplotlib window and continuously generates plots of hop along iterations.

    Each update will calculate `n_iters` iterations of the hop along function
    (`hop_along_eq`) for parameters (`a`, `b`, `c`) and draw them on screens.
    Once drawn on screen, the points will remain drawn for `n_hist` future updates,
    with their alpha decreasing linearly with each update.
    A new update will be calcualted every 0.04s (25 fps).

    There is currently no way to make this return so good luck.

    Args:
        a (float):
            Hop along parameter.
        b (float):
            Hop along parameter.
        c (float):
            Hop along parameter.
        n_iters (int):
            The number of hop along iterations to draw per frame/update.
        n_hist (int):
            The number of frames/updates that an interation should remain on screen.
        n_reset (int):
            If n_reset > 0, it is the number of frames to be calculated before
            a new set of parameters (a,b,c) are generated.
        alpha_init (float, optional):
            Initial alpha value for points. Defaults to 0.3.
        pause_time (float, optional):
            Time to pause between frames (controls frame-rate). Defaults to 0.9.
    """
    # TODO figure out how to stop annoying white boarder on top and left.
    matplotlib.use("Qt5agg")
    plt.style.use("dark_background")
    plt.ion()

    # Store previous iterations in a list which we will use as a fifo system.
    history = []

    values = np.array([[0.0, 0.0]])
    values = np.swapaxes(values, 0, 1)
    full_iters = 0
    positive_reset = n_reset > 0
    positive_hist = n_hist > 0
    while True:
        # Draw next iter.
        values = hop_along_for_n(a, b, c, n_iters, xy_init=values[:, -1])
        values = np.swapaxes(values, 0, 1)
        plt.scatter(
            values[0],
            values[1],
            marker="*",
            c=list(range(0, n_iters)),
            alpha=alpha_init,
            cmap="plasma",
        )
        # Draw previous iters.
        if positive_hist:
            for index, arr in enumerate(history):
                alpha = (index + 1) / n_hist * alpha_init
                plt.scatter(
                    arr[0],
                    arr[1],
                    marker="*",
                    c=list(range(0, n_iters)),
                    alpha=alpha,
                    cmap="plasma",
                )
            # Pop the first entry.
            history.append(values)
            history = history[-n_hist:]

        plt.xticks([])
        plt.yticks([])
        plt.pause(pause_time)
        plt.clf()

        full_iters += 1
        if positive_reset and (full_iters % n_reset == 0):
            values = np.array([[0.0, 0.0]])
            values = np.swapaxes(values, 0, 1)
            a, b, c = random_abc()


def _main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Run hop along visualiser",
        epilog=(
            "`--nreset 1` creates a very chaotic (but cool) visual effect. "
            "Larger numbers (e.g. 10) creates more stable structures."
        ),
    )

    parser.add_argument(
        "--niters",
        nargs="?",
        default=1_000,
        type=int,
        help="number of hop along iterations drawn per frame (default 1000)",
    )
    parser.add_argument(
        "--nhist",
        nargs="?",
        default=10,
        type=int,
        help="number of frames that an iteration should remain on-screen (default 10)",
    )
    parser.add_argument(
        "--nreset",
        nargs="?",
        default=10,
        type=int,
        help=(
            "number of frames generated before parameters are randomised, "
            "setting to zero keeps the same parameters throughout (default 10)"
        ),
    )
    parser.add_argument(
        "--fps",
        nargs="?",
        default=25.0,
        type=float,
        help="number of frames generated per second (default 25)",
    )

    parsed = parser.parse_args()

    n_iters = parsed.niters
    n_hist = parsed.nhist
    n_reset = parsed.nreset
    fps = parsed.fps
    pause_time = 1.0 / fps

    print(f"{n_iters=}\n{n_hist=}\n{n_reset=}\n{fps=}\n{pause_time=}")

    plot_hop_along(
        *random_abc(),
        n_iters=n_iters,
        n_hist=n_hist,
        n_reset=n_reset,
        pause_time=pause_time,
    )


if __name__ == "__main__":
    _main()
