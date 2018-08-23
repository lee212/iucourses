import os
import sys
import yaml
import argparse

"""
TODO: sort
TODO: editing
TODO: import/export between rst/yml
TODO: trigger to generate (automation)
TODO: documentation for general guide
"""
class generateRST(object):

    space = "   "

    base_info = "base.yml"

    def parse_argument(self):
        parser = argparse.ArgumentParser("generate rst from yaml data")
        parser.add_argument("-f", dest="fname", help="yaml file")
        parser.add_argument("-d", dest="directory", help="lecture directory")
        args = parser.parse_args()

        if args.directory and args.directory[0] != "/":
            dirname = os.getcwd()
            args.directory = os.path.join(dirname, args.directory)
        self.args = args
        self.argparser = parser
        return args

    def load_yaml(self, fname=None):
        if not fname:
            fname = self.args.fname
        with open(fname) as f:
            ymldata = yaml.load(f)
        return ymldata

    def load_course(self):
        base = os.path.join(self.args.directory, self.base_info)
        with open(base) as f:
            bdata = yaml.load(f)

        bdata['title'] = "{} ({},{})".format(bdata['title'],
                bdata['course_number'], bdata['semester'])

        bdata['lectures'] = self._load_materials(bdata['lectures'])
        bdata['assignments'] = self._load_materials(bdata['assignments'])
        return bdata

    def _load_materials(self, mlist):
        mdata = []
        for fname in mlist:
            fpath = os.path.join(self.args.directory, fname)
            mdata.append(self.load_yaml(fpath))

        # Special case
        ndata = {}
        nidx = 0
        for m in mdata:
            for k, entry in m['materials'].items():
                ndata[nidx] = entry
                nidx += 1
        return ndata

    def gen_table(self, title=None, header=None, options=None):
        res = ".. list-table:: %(title)s\n" + \
                "%(options)s\n" + \
                "\n" + \
                "%(header)s\n" + \
                "%(body)s"
        title = title or self.ymldata['title']
        self.table_header = header
        header = self.render_header(header)
        options = self.render_options(options)
        body = self.render_body()
        nres = res % vars()
        print (nres)

    def render_header(self, header):
        nheader = ""
        for h in header:
            nheader += self.space  + "  - " + h.title() + "\n"
        header = self.space + "*" + nheader[len(self.space) + 1:]
        return header

    def render_options(self, options):
        noptions = ""
        for opt, val in options.items():
            noptions += self.space + ":{}: {}\n".format(opt, val)
        return noptions

    def render_body(self, body=None):

        lectures = ""
        assignments = ""

        if body:
            materials = body
        else:
            if 'lectures' in self.ymldata:
                lectures = self._render_materials(self.ymldata['lectures'])
            if 'assignments' in self.ymldata:
                assignments = self._render_materials(self.ymldata['assignments'])

        materials = lectures + assignments
        return materials

    def _render_materials(self, materials):
        nbody = ""
        for k, entry in materials.items():
            mbody = ""
            try:
                for header in self.table_header:
                    if header in entry:
                        val = entry[header]
                    else:
                        val = ""
                    if val[:4] == "http":
                        val = "`Link <{}>`_".format(val)
                    if header == "topic":
                        val = "**" + val.title() + "**"
                    if header == "media" and isinstance(val, list):
                        nvals = ""
                        for item in val:
                            extra = ""
                            if item['type'] == "video":
                                nvals += "`Play ({}) <{}>`_ | ".format( 
                                        item['length'], item['source'])
                            elif item['type'] == "pdf":
                                if 'misc' in item:
                                    extra = "({})".format(item['misc'])
                                nvals += "`PDF {} <{}>`_ | ".format(
                                        extra, item['source'])
                            elif item['type'] == "ppt":
                                if 'misc' in item:
                                    extra = "({})".format(item['misc'])
                                nvals += "`PPT {} <{}>`_ | ".format(
                                        extra, item['source'])
                        if nvals[-2:] == "| ":
                            nvals = nvals[:-2]
                        val = nvals
                    mbody += self.space + "  - {}\n".format(val)
            except Exception as e:
                print (e, sys.exc_info())
                continue
            nbody += self.space + "*" + mbody[len(self.space) + 1:]
        return nbody

if __name__ == "__main__":
    rstgen = generateRST()
    args = rstgen.parse_argument()
    if args.fname:
        ymldata = rstgen.load_yaml()
        rstgen.ymldata = ymldata
        rstgen.gen_table(title="Cloud Computing", 
                header=["topic", "video", "slide", "length", "type", "chapter", "part"], 
                options = { "widths": "30 10 10 10 10 10" ,
                    "header-rows": 1})
    elif args.directory:
        ymldata = rstgen.load_course()
        rstgen.ymldata = ymldata
        rstgen.gen_table(header=["topic", "media", "section", "type"], 
                options = { "widths": "30 10 10 10", 
                    "header-rows": 1})

