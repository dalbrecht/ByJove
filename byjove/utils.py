import argparse
import os
from typing import Any, Dict


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog="byjove",
        description="ByJove converts Jupyter Notebooks in to markdown files and assets",
    )
    parser.add_argument("filename")
    parser.add_argument(
        "-v", "version", default=5, help="Jupyter Version of the ipynb file"
    )
    parser.add_argument(
        "-o",
        "output_file",
        default=None,
        help="Output Filename To Use, defaults to the input file name with .ipynb replaced with .md",
    )
    parser.add_argument(
        "-p", "output_path", default="./rendered", help="Path For the Output File"
    )
    parser.add_argument(
        "-r",
        "resource_path",
        default="resources",
        help="Path For the resources directory for the file",
    )
    return parser


def build_config_from_args(args: argparse.Namespace) -> Dict[str, Any]:
    config: Dict[str, Any] = dict()
    config["filename"] = os.path.splitext(args.filename)[0]
    config["path"] = args.filename
    config["version"] = args.version
    config["resource_path"] = args.resource_path
    if args.output_file is None:
        config["output_file"] = args.filename.split(os.pathsep)[-1] + ".md"
    else:
        config["output_file"] = args.output_file

    config["output_path"] = args.output_path
    return config
