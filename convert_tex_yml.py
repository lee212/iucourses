import os 
import csv
import yaml
import argparse
import datetime
from collections import defaultdict
from pprint import pprint

class convertLatex(object):

    template = { "video": ["type", "length", "topic", "source"],
            "slides": ["type", "misc", "topic", "source"] }

    materials = {} #defaultdict(list)

    def parse_argument(self):
        parser = argparse.ArgumentParser("convert latex elements to yaml")
        parser.add_argument("-f", dest="fname", help="filename of latex")
        parser.add_argument("-t", dest="title", help="title of the chapter")
        parser.add_argument("-T", dest="type", help="lecture|assignment")
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
            for col_idx in range(len(row)):
                col_name = self.template[row[0]][col_idx]
                col_val = row[col_idx]
                row_dict[col_name] = col_val
            # special case
            if row_dict['type'] == "slides":
                row_dict['type'] = "pdf"
                if row_dict['topic'].find(" - ppt") > 0:
                    row_dict['type'] = "ppt"
            elif 'length' in row_dict:
                row_dict['length'] = \
                        str(datetime.datetime.strptime(row_dict['length'],
                                '%M:%S').time())
            if row[0] == "video":
                entry = { "media": [row_dict],
                        "section": self.args.title,
                        "topic": row_dict['topic'],
                        "type": self.args.type}
                rid += 1
            else:
                entry['media'].append(row_dict)

            self.materials[rid] = entry
        return self.materials

    def save_yml(self, outfname=None, data=None):
        if not data:
            data = {"materials": self.materials}
        if not outfname:
            outfname, ext = os.path.splitext(self.args.fname)
            outfname += ".yml"
        with open(outfname, "w") as f:
            yaml.dump(data, f, default_flow_style = False)

if __name__ == "__main__":
    obj = convertLatex()
    obj.parse_argument()
    obj.convert()
    obj.save_yml()
