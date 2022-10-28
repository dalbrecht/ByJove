import argparse
from byjove import convert_file
from byjove.utils import build_arg_parser, build_config_from_args


def convert():
    arg_parser = build_arg_parser()
    parsed_namespace = arg_parser.parse_args()
    config = build_config_from_args(parsed_namespace)
    convert_file(config)


if __name__ == "__main__":
    convert()
