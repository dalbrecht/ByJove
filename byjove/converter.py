import argparse
import nbformat


def convert_markdown_cell(markdown_cell, _):
    include_following_code = False
    if "[//]: #" in markdown_cell['source']:
        include_following_code = True

    return markdown_cell["source"], include_following_code


def convert_code_cell(code_cell, include_code):
    print(code_cell)
    out_str = ""

    if include_code:
        out_str = f"```python{code_cell['source']}```"

    return out_str, False


def convert_cell(cell, forward_include: bool):
    # print(cell)
    if cell["cell_type"] == 'markdown':
        return convert_markdown_cell(cell, forward_include)
    else:
        return convert_code_cell(cell, forward_include)


def convert_file(path: str, version=4):
    with open(path) as f:
        notebook = nbformat.read(f, as_version=version)
    out = ""
    forward = False
    for cell in notebook['cells']:
        print(cell)

        md_str, forward = convert_cell(cell, forward)
        out = out + md_str

    print(out)


convert_file("../notebooks/basic_test.ipynb")
