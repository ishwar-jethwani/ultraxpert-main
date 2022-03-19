from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
import json
from user.models import *
from payment.models import *
from activity.models import *
from events.models import *
from datetime import datetime
def dashboard(request):
    return render(request,"support/base.html")

class DashboardView(APIView):
    template_name = 'support/dashboard.html'
    ctx = {}
    base_context = None

    # main function of get document
    def get(self, request):
        self.data = request.GET
        if 'action' in self.data:
            action = int(self.data['action'])
            action_mapper = {1:self.get_user_table}
            status = action_mapper.get(action, lambda: 'Invalid')()
            if status == 'Invalid':
                self.ctx = {'status': 'error', 'msg': 'Invalid Action'}
            return Response(self.ctx)
        return self.base_context.render(request, self.template_name)
    def get_user_table(self):
        self.params = json.loads(self.data['params'])
        search = self.params['search']
        users = User.objects.all()
        if not search == "":
            users = users.filter(email__icontains=search)
        count = users.count()

        arr = []
        for user in users:
            new_dict = {
                "id":user.user_id,
                "name": f'<a class="" style="cursor:pointer" data-id="{user.pk}"><h4 class="p-0 m-0 text-bold text-secondary" ">' + str(user.email)+ '</h4>' + '</a>',
                "Joined_on": datetime.strftime(user.date_joined, "%b %d,%Y"),
                "action": f'<select class="form-control m-0 document-option" style="cursor:pointer" data-name="{user.username }" data-id="{user.pk}"><option value="">Select Action </option><option value="2">Edit</option><option value="3">Make a Copy</option><option value="5">Preview</option><option class="text-danger" value="6">Delete</option></select>',
            }
            arr.append(new_dict)
        self.ctx.update({'data': arr, 'count': count})

