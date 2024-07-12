import subprocess
import attrs


@attrs.frozen
class DataWithLevel:
    content: str
    depth: int


test = """
Income
   Revenue
      IAP
      Ads
   Other-Income
Expenses
   Developers
      In-house
      Contractors
   Advertising
   Other Expenses
"""


def parse_indented_hierachy(data: str, indentation: int = 2) -> dict:
    hierachy_data = {}
    stack = []
    for line in data.splitlines():
        if not line.strip():
            continue
        content = line.rstrip()  # drop \n
        row = content.split(" " * indentation)
        stack[:] = stack[:len(row) - 1] + [row[-1]]
        # generate nested dict
        hdata = hierachy_data
        for item in stack:
            try:
                key, val = item.split(":")
            except:
                breakpoint()
            if not val:
                hdata = hdata.setdefault(item, {})
            else:
                hdata[key] = val
    return hierachy_data



def get_item(item: str) -> dict:
    completed = subprocess.run(["op", "item", "get", item], stdout=subprocess.PIPE)
    entries = [entry for entry in completed.stdout.decode("utf-8").split("\n") if entry.strip()]




