from django.shortcuts import render
import numpy as np
from nltk import word_tokenize

from Resume.models import Resume
from User.models import User
import pandas as pd
import numpy as np
import pandas as pd
from django.shortcuts import render
import numpy as np
from Resume.models import Resume
from User.models import User
from django.db.models import Q
from nltk.corpus import stopwords
import tensorflow
import keras


from Main import primitive_tagger as ptt
from Main import tag_matching as tm

stop_words = list(stopwords.words('english'))
# stop_words = list(get_stop_words('en'))  # About 900 stopwords
nltk_words = list(stopwords.words('english'))  # About 150 stopwords
stop_words.extend(nltk_words)


def req_res(data):
    return data['id', 'user_id']


def extract_technical_tags(txt):
    # list1 = word_tokenize(txt)
    # return [w for w in list1 if not w in stop_words]
    return ptt.custom_tagger(txt)


def extract_human_tags(txt):
    # list1 = word_tokenize(txt)
    # return [w for w in list1 if not w in stop_words]
    return ptt.custom_tagger(txt)


def results(request, resume_id):
    user_id = Resume.objects.filter(id=resume_id)

    # print(ptt.custom_tagger('c++,java,english,programming,math'))
    q1 = Resume.objects.all().values()
    dfResumes = pd.DataFrame.from_records(q1)

    q2 = User.objects.all().values()
    dfUsers = pd.DataFrame.from_records(q2)
    dfUsers = dfUsers.rename(index=str, columns={"id": "user_id"})

    all_data = pd.merge(dfUsers, dfResumes, on='user_id', how='inner')

    # ..........................................................................

    # technical

    to_process_users = all_data[np.logical_not( all_data['was_processed_x'])][['user_id', 'skills']]

    for index, row in to_process_users.iterrows():
        t = User.objects.get(id=row['user_id'])
        t.skills_processed = extract_technical_tags(row['skills'])
        t.was_processed = True
        t.save()

    to_process_resume = all_data[np.logical_not(all_data['was_processed_y'])][['id', 'text']]

    for index, row in to_process_resume.iterrows():
        t = Resume.objects.get(id=row['id'])
        t.text_filtered = extract_human_tags(row['text'])
        t.was_processed = True
        t.save()



    # print(to_process_users)

    # res = all_data[['user_id', 'was_processed_x']]
    # ..........................................................................

    all_data['geo'] = all_data.apply(lambda x: None)
    all_data['type'] = all_data['type'].apply(lambda x: 'mentor' if x == '1' else 'student')

    all_data.rename(index=str, columns={"text_filtered" : "intro_phrase_tags",
                                        "skills_processed" : "skills_tags",
                                        "type" : "user_role"},inplace=True)

    best_people = tm.process_by_id(all_data, int(resume_id))
    print(all_data)
    if (not(best_people is None)):
        print('----------------------------------')

        print(best_people)


    #df = pd.DataFrame({'id' : [1], 'user_id' : [1]})#req_res(all_data)


    # ..........................................................................
        resumes = Resume.objects.filter(id__in=list(best_people["id"]))
        users = User.objects.filter(id__in=list(best_people["user_id"]))
        return render(request, 'matching.html', {'resumes': resumes, 'users': users})
    else:
        print("VU GAY")
        return render(request, 'main.html')


def main(request):
    return render(request, 'main.html')


# def results(request, resume_id):
#     # q = Resume.objects.all().values()
#     # dfResumes = pd.DataFrame.from_records(q)
#     q1 = Resume.objects.all().values()
#     dfResumes = pd.DataFrame.from_records(q1)
#     q2 = User.objects.all().values()
#     dfUsers = pd.DataFrame.from_records(q2)
#     dfUsers = dfUsers.rename(index=str, columns={"id": "user_id"})
#     all_data = pd.merge(dfUsers, dfResumes, on='user_id', how='inner')
#     print(all_data)
#     # Call backend function returns resumes' ids and users' ids
#     list = np.array([(1, 2), (2, 3), (2, 2)])
#     resumes_ids = list.T[0]
#     users_ids = list.T[1]
#
#     resumes = Resume.objects.filter(id__in=resumes_ids)
#     users = User.objects.filter(id__in=users_ids)
#     return render(request, 'matching.html', {'resumes': resumes, 'users': users})