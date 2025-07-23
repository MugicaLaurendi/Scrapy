class MyCustomMiddleware:
    def process_request(self, request, spider):
        # Modify the request here if needed
        return None

    def process_response(self, request, response, spider):
        # Modify the response here if needed
        return response

    def process_exception(self, request, exception, spider):
        # Handle exceptions here if needed
        return None