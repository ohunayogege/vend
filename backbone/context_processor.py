from .models import APISetting, AirtimeToCashCalc, WebsiteConfig

def WebsiteSetup(request):
    api = APISetting.objects.last()
    web = WebsiteConfig.objects.last()
    a2c = AirtimeToCashCalc.objects.last()

    return {
        'api': api,
        'website': web,
        'a2c': a2c,
    }
