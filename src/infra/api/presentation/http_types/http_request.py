class HttpRequest:
    def __init__(self,
                 a_headers=None,
                 a_body=None,
                 a_query_params=None,
                 a_path_params=None,
                 an_url=None,
                 an_ipv4=None):
      self.headers = a_headers
      self.body = a_body
      self.query_params = a_query_params
      self.path_params = a_path_params
      self.url = an_url
      self.ipv4 = an_ipv4

