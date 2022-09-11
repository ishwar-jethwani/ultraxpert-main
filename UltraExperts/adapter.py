from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.reffered_by = data.get('reffered_by')
        user.is_verified = data.get("verication_satus")
        user.save()
        return user