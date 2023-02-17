
from django.views.generic import TemplateView

from .models import License

class AccountView(TemplateView):
	template_name = 'account.html'
	
	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		license, _ = License.objects.get_or_create(user=self.request.user)

		data['license_short_text'] = license.license_short_text
		data['license_text'] = license.license_text

		return data
	
	def post(self, request):
		license, _ = License.objects.get_or_create(user=request.user)
		
		try:
			license.license_short_text = request.POST['license_short_text']
		except:
			pass

		try:
			license.license_text = request.POST['license_text']
		except:
			pass

		license.save()

		return self.get(request)
