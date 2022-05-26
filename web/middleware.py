


from django.shortcuts import redirect


class UserHasTransaction:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated == True:
            if request.user.is_superuser == False:
                if request.user.transaction_pin == '' or request.user.transaction_pin == None:
                    return redirect("settings")

                # response = self.get_response(request)
                # return response