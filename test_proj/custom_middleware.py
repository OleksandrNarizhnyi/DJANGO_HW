class CustomMiddleware:
    def __init__(self, get_response):
        self.resp = get_response

    def __call__(self, request):
        print("ДО ОБРАБОТКИ ЗАПРОСА ==========================")

        response = self.resp(request)

        print("ПОСЛЕ ОБРАБОТКИ ЗАПРОСА ==========================")

        return response