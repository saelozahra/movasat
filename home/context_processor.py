from django.contrib.sites.shortcuts import get_current_site


def site(request):
    current_site = get_current_site(request)
    context = {
        "site_name": "قرارگاه جهادی شهید حاج قاسم سلیمانی",
        # "home_url": "http://jahadi.hajghasem.ir",
        "home_url": f"http://{current_site.domain}",
    }
    return context
