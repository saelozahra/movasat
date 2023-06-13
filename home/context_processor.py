
def site(request):
    context = {
        "site_name": "قرارگاه جهادی شهید حاج قاسم سلیمانی",
        # "home_url": "http://jahadi.hajghasem.ir",
        "home_url": "http://127.0.0.1:8004",
    }
    return context
