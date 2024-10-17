from django.views.generic import ListView
from django.http import Http404
from jobs.utils import q_search
from users.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CatalogView(ListView):
    model = User
    template_name = 'jobs/catalog.html'
    context_object_name = 'users'
    paginate_by = 6
    allow_empty = False

    def get_queryset(self):
        slug_url = self.kwargs.get('slug_url', None)
        query = self.request.GET.get('q')
        available = self.request.GET.get('available')
        order_by = self.request.GET.get('order_by')

        if slug_url == 'all':
            users = User.objects.all()
        elif query:
            users = q_search(query)
        else:
            users = User.objects.filter(skills__slug=slug_url)

        if available == 'on':
            users = users.filter(is_free=True)

        if order_by == 'username':
            users = users.order_by('username')
        else:
            users = users.order_by('id')

        if not users.exists():
            raise Http404('Пользователи не найдены.')

        return users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users_list = self.get_queryset()
        paginator = Paginator(users_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        context['users'] = users
        context['title'] = 'HandyHub - Каталог'
        context['slug_url'] = self.kwargs.get('slug_url')
        return context
