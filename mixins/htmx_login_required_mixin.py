from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


class HTMXLoginRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        if self.request.headers.get("HX-Request"):
            response = HttpResponse()
            response["HX-Trigger"] = "openLoginModal"
            response["HX-Reswap"] = "none"
            print("Handle htmx required mixin")
            return response

        main_url = reverse("main:index")
        return HttpResponseRedirect(f"{main_url}?login_required=1")
