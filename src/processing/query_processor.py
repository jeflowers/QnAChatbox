class QueryProcessor:
    def __init__(self, query_engine):
        self.query_engine = query_engine

    def process_query(self, message):
        return self.query_engine.query(message)

    def stream_response(self, message):
        response = self.query_engine.query(message)
        for text in response.response_gen:
            yield text