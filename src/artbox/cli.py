"""Cli functions to define the arguments and to call Makim."""
import argparse
import sys

from artbox import __version__
from artbox.sounds import Sound
from artbox.videos import Video, Youtube
from artbox.voices import Voice


class CustomHelpFormatter(argparse.RawTextHelpFormatter):
    """Formatter for generating usage messages and argument help strings.

    Only the name of this class is considered a public API. All the methods
    provided by the class are considered an implementation detail.
    """

    def __init__(
        self,
        prog,
        indent_increment=2,
        max_help_position=4,
        width=None,
        **kwargs,
    ):
        """Define the parameters for the argparse help text."""
        super().__init__(
            prog,
            indent_increment=indent_increment,
            max_help_position=max_help_position,
            width=width,
            **kwargs,
        )


def _get_args():
    """Define the arguments for the CLI."""
    parser = argparse.ArgumentParser(
        prog="ArtBox",
        description="A set of tools for handling multimedia files.",
        epilog=(
            "If you have any problem, open an issue at: "
            "https://github.com/ggpedia/artbox"
        ),
        formatter_class=CustomHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show the version of the installed MakIm tool.",
    )
    parser.add_argument(
        "runner",
        default=None,
        help=(
            "Specify the runner to be performed. "
            "\nOptions are: audio, sounds, and video."
        ),
    )
    parser.add_argument(
        "method",
        default=None,
        help=("Specify the runner method to be performed."),
    )
    return parser


def extract_artbox_args():
    """Extract artbox arguments from the CLI call."""
    artbox_args = {}
    index_to_remove = []

    for ind, arg in enumerate(list(sys.argv)):
        if arg in [
            "--help",
            "--version",
        ]:
            continue

        if not arg.startswith("--"):
            continue

        index_to_remove.append(ind)

        arg_name = None
        arg_value = None

        next_ind = ind + 1

        arg_name = sys.argv[ind][2:]

        if (
            len(sys.argv) == next_ind
            or len(sys.argv) > next_ind
            and sys.argv[next_ind].startswith("--")
        ):
            arg_value = True
        else:
            arg_value = sys.argv[next_ind]
            index_to_remove.append(next_ind)

        artbox_args[arg_name] = arg_value

    # remove exclusive artbox flags from original sys.argv
    for ind in sorted(index_to_remove, reverse=True):
        sys.argv.pop(ind)

    return artbox_args


def show_version():
    """Show version."""
    print(__version__)


def app():
    """Call the artbox program with the arguments defined by the user."""
    artbox_args = extract_artbox_args()

    args_parser = _get_args()
    args = args_parser.parse_args()

    if args.version:
        return show_version()

    if args.runner == "sound":
        runner = Sound(artbox_args)
    elif args.runner == "voice":
        runner = Voice(artbox_args)
    elif args.runner == "video":
        runner = Video(artbox_args)
    elif args.runner == "youtube":
        runner = Youtube(artbox_args)

    return getattr(runner, args.method.replace("-", "_"))()
