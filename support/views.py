from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
import json
from user.models import *
from payment.models import *
from activity.models import *
from events.models import *


class DashboardView(APIView):
    template_name = 'dashboard.html'
    ctx = {}
    base_context = None
    permission_classes = [IsAdminUser]

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
        # self.offset = int(self.params['offset'])
        # self.limit = int(self.params.get('limit', 10))
        # self.page = int(self.offset / self.limit)
        users = User.objects.all()
        if not search == "":
            users = users.filter(p_name__icontains=search)
        count = users.count()
        # products= Paginator(products, self.limit)
        # products= products.page(self.page + 1)

        arr = []
        for user in users:
            new_dict = {
                "id":user.user_id,
                'name': f'<a class="" style="cursor:pointer" data-id="{user.id}"><h4 class="p-0 m-0 text-bold text-secondary" ">' + user.email + '</h4>' + '</a>',
                "Joined_on": datetime.datetime.strftime(user.date_joined, "%b %d,%Y"),
                "action": f'<select class="form-control m-0 document-option" style="cursor:pointer" data-name="{user.username }" data-id="{user.id}"><option value="">Select Action </option><option value="2">Edit</option><option value="3">Make a Copy</option><option value="5">Preview</option><option class="text-danger" value="6">Delete</option></select>',
            }
            arr.append(new_dict)
        self.ctx.update({'data': arr, 'count': count})

