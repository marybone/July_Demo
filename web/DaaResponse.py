import uuid
from web import DaaStatus


class DaaResponse(object):
    # def __init__(self):
    #     self.__init__(self, DaaStatus.SUCCESS, "")
    #
    #
    # def __init__(self, content):
    #     self.__init__(self, DaaStatus.SUCCESS, content)
    #

    def __init__(self, status, content):
        self.status = status
        self.id = str(uuid.uuid4())
        self.content = content
