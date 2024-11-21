class HttpResponse:
    def __init__(self,
                 a_status_code=None,
                 a_body=None,
              ):
      self.status_code = a_status_code
      self.body = a_body
