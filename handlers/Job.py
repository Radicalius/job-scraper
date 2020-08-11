class Job:

    def __init__(self, title, comp, loc, desc, url):
        self.title = title
        self.comp = comp
        self.loc = loc
        self.desc = desc
        self.url = url

    def __str__(self):
        return str({
            "title": self.title,
            "comp": self.comp,
            "loc": self.loc,
        })

    def __repr__(self):
        return str(self)

    def write_to_csv(self, writer):
        writer.writerow(
            [
                self.title,
                self.comp,
                self.loc,
                self.desc,
                self.url
            ]
        )
