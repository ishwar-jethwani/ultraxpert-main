from allauth.account.adapter import DefaultAccountAdapter

#Adapter For Custom Account
class CustomAccountAdapter(DefaultAccountAdapter):
    """Saving User Object"""
    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.reffered_by = data.get('reffered_by') 
        user.is_verified = data.get("verification_status")
        user.save()
        return user