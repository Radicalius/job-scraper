class Handler:

    type = "generic"

    def get_num_pages(self):
        return 0

    def scan_page(self,n):
        return [{}]

    def scan_posting(self,meta):
        return Job(
            "", "", "", "", ""
        )
