import falcon


class HTTP_OK_ERROR(falcon.HTTPError):
    def __init__(self, title, message):

        super().__init__(status="200 OK")
        self._title = title
        self._thestatus = "ERROR"
        self._message = message

    def to_dict(self, obj_type=dict):
        result = super().to_dict(obj_type)
        result['title'] = self._title
        result['message'] = self._message
        result['status'] = self._thestatus
        return result
