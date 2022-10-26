import argparse
import nbformat
import os
import base64

config = {
    "output_path": "../output/tests/rendered/",
    "resource_path": "resources",
    "asset_counter": 0,
}

ASSET_COUNTER = 0


def store_base64_resource(resource_blob, mimetype, config):
    config["asset_counter"] += 1
    out_bytes = base64.b64decode(resource_blob)
    mime_to_extension = {"image/png": ".png", "image/jpeg": ".jpg"}

    file_name = f"{config['file_name']}_asset_{config['asset_counter']:03}{mime_to_extension[mimetype]}"
    out_path = os.path.join(config["output_path"], config["resource_path"], file_name)
    with open(out_path, "wb") as out_file:
        out_file.write(out_bytes)
    return file_name


def convert_markdown_cell(markdown_cell, *args, **kwargs):
    include_following_code = False
    if "[//]: #" in markdown_cell["source"]:
        include_following_code = True

    return markdown_cell["source"], include_following_code


def convert_code_cell(code_cell, include_code, config):
    out_str = ""

    if include_code:
        out_str = f"```\npython{code_cell['source']}\n```"

    for output in code_cell.outputs:
        if "data" in output.keys():
            if "text/html" in output["data"]:
                out_str += output["data"]["text/html"]
            elif "image/png" in output["data"]:
                file_name = store_base64_resource(
                    resource_blob=output["data"]["image/png"],
                    mimetype="image/png",
                    config=config,
                )
                img_string = f"![{output['data']['text/plain']}]({config['resource_path']}/{file_name})"
                out_str += "\n" + img_string + "\n"
    return out_str, False


def convert_cell(cell, config, forward_include: bool = False):
    # print(cell)
    if cell["cell_type"] == "markdown":
        return convert_markdown_cell(cell, forward_include, config)
    else:
        return convert_code_cell(cell, forward_include, config)


def convert_file(path: str, file_name=None, version=4):
    if file_name is None:
        file_name = path.split(os.pathsep)[-1]
        config["file_name"] = os.path.splitext(file_name)[0]
    else:
        config["file_name"] = file_name
    with open(path) as f:
        notebook = nbformat.read(f, as_version=version)
    out = ""
    forward = False
    for cell in notebook["cells"]:
        md_str, forward = convert_cell(
            cell=cell, config=config, forward_include=forward
        )
        out = out + md_str

    out_file_name = file_name + ".md"
    with open(os.path.join(config["output_path"], out_file_name), "w") as o:
        o.write(out)


convert_file("../notebooks/basic_test.ipynb", "basic_test")
