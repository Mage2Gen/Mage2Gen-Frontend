from django.test import Client, TestCase
from django.urls import reverse

GOOGLE_BEGIN = "social:begin"
GOOGLE_BACKEND = "google-oauth2"


class GoogleSocialLoginTests(TestCase):
    def test_get_social_begin_is_not_allowed(self):
        response = self.client.get(self._begin_url())
        self.assertEqual(response.status_code, 405)

    def test_home_renders_post_login_forms(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        begin_url = self._begin_url()
        self.assertEqual(html.count(f'<form method="post" action="{begin_url}">'), 2)
        self.assertGreaterEqual(html.count('name="csrfmiddlewaretoken"'), 2)
        self.assertIn('type="submit"', html)
        self.assertIn("Sign in with Google", html)

    def test_post_with_csrf_redirects_to_google(self):
        client = Client(enforce_csrf_checks=True)
        token = self._csrf_token(client)
        response = client.post(
            self._begin_url(),
            {"csrfmiddlewaretoken": token},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("https://accounts.google.com/", response["Location"])

    def _begin_url(self):
        return reverse(GOOGLE_BEGIN, kwargs={"backend": GOOGLE_BACKEND})

    def _csrf_token(self, client):
        response = client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("csrftoken", client.cookies)
        return client.cookies["csrftoken"].value
