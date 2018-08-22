import csv
import yaml
import argparse
from collections import defaultdict
from pprint import pprint

class convertLatex(object):

    template = { "video": ["type", "length", "topic", "source"],
            "slides": ["type", "misc", "topic", "source"] }

    media = defaultdict(list)

    def parse_argument(self):
        parser = argparse.ArgumentParser("convert latex elements to yaml")
        parser.add_argument("-f", dest="fname", help="filename of latex")
        args = parser.parse_args()
        self.arg_parser = parser
        self.args = args
        return args

    def convert(self):
        fname = self.args.fname
        with open(fname) as f:
            data = list(csv.reader(f, delimiter=","))

        rid = -1
        for row in data:
            row_dict = {}
            if row[0] == "video":
                rid += 1
            for col_idx in range(1, len(row)):
                col_name = self.template[row[0]][col_idx]
                col_val = row[col_idx]
                row_dict[col_name] = col_val
            self.media[rid].append(row_dict)
        return self.media

if __name__ == "__main__":
    obj = convertLatex()
    obj.parse_argument()
    media = obj.convert()
    pprint (dict(media), indent=4)
