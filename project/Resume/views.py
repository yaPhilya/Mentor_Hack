from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView
from Resume.form import ResumeCreationForm


class NewResume(FormView):
    template_name = 'create_resume.html'
    form_class = ResumeCreationForm
    # success_url = 'users:userpage'

    def get_success_url(self):
        return reverse("users:userpage", kwargs={'u_id': self.request.user.id})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.text_filtered = "0"
        # form.instance.was_processed = '0'
        form.save()
        return super(NewResume, self).form_valid(form)