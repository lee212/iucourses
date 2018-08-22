import yaml
import argparse

class generateRST(object):
    space = "   "

    def parse_argument(self):
        parser = argparse.ArgumentParser("generate rst from yaml data")
        parser.add_argument("-f", dest="fname", help="yaml file")
        args = parser.parse_args()

        self.args = args
        self.argparser = parser
        return args

    def load_yaml(self):
        with open(self.args.fname) as f:
            ymldata = yaml.load(f)
        self.ymldata = ymldata
        return ymldata

    def gen_table(self, title, header=None, options=None):
        res = ".. list-table:: %(title)s\n" + \
                "%(options)s\n" + \
                "\n" + \
                "%(header)s\n" + \
                "%(body)s"
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
            noptions += self.space + ":{}: {}".format(opt, val)
        return noptions

    def render_body(self, body=None):
        if body:
            materials = body
        else:
            materials = self.ymldata['materials']
        nbody = ""
        for material in materials:
            mbody = ""
            try:
                for header in self.table_header:
                    if header in material:
                        val = material[header]
                    else:
                        val = ""
                    if val[:4] == "http":
                        val = "`Link <{}>`_".format(val)
                    if header == "topic":
                        val = "**" + val.title() + "**"
                    elif header == "video":
                        val = val.replace("Link", "Play", 4)
                    elif header == "slide":
                        val = val.replace("Link", "Slide", 4)
                    mbody += self.space + "  - {}\n".format(val)
            except:
                continue
            nbody += self.space + "*" + mbody[len(self.space) + 1:]
        return nbody

if __name__ == "__main__":
    rstgen = generateRST()
    args = rstgen.parse_argument()
    rstgen.load_yaml()
    rstgen.gen_table(title="Cloud Computing", 
            header=["topic", "video", "slide", "length", "type", "chapter", "part"], 
            options = { "widths": "30 10 10 10 10 10" })

