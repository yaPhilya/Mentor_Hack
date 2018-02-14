from django.shortcuts import render
import numpy as np
from Resume.models import Resume
from User.models import User


def main(request):
    return render(request, 'main.html')


def results(request, resume_id):
    # Call backend function returns resumes' ids and users' ids
    list = np.array([(1, 2), (2, 3), (2, 2)])
    resumes_ids = list.T[0]
    users_ids = list.T[1]
    resumes = Resume.objects.filter(id__in=resumes_ids)
    users = User.objects.filter(id__in=users_ids)
    return render(request, 'matching.html', {'resumes': resumes, 'users': users})