import json
import os


class Converter:
    def __init__(self, notebook_string):
        self._parsed = json.loads(notebook_string)

    @property
    def md(self):
        output = ""
        placeholders = False
        for block in self._parsed["cells"]:
            if block["cell_type"] == "markdown":
                content = block["source"]
                if "{code}" in content:
                    placeholders = True
                else
            elif block["cell_type"] == "code":
                if placeholders:
                    content


if __name__ == "__main__":
    with open("../notebooks/basic_test.ipynb", "r") as nb:
        loaded_string = nb.read()
