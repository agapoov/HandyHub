from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'


class AboutView(TemplateView):
    template_name = 'main/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HandyHub - About Us'
        return context


class ContactView(TemplateView):
    template_name = 'main/contact_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HandyHub - Contact Info'
        return context
