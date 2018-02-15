# import numpy as np
# import pandas as pd
#
# from django.shortcuts import render
# import numpy as np
# from Resume.models import Resume
# from User.models import User
# from django.db.models import Q
# from nltk.corpus import stopwords
#
# stop_words = list(get_stop_words('en'))         #About 900 stopwords
# nltk_words = list(stopwords.words('english')) #About 150 stopwords
# stop_words.extend(nltk_words)
#
# def req_res(data):
#     return data['id', 'user_id']
#
# def extract_technical_tags(txt):
#     list1 = word_tokenize(txt)
#     return [w for w in list1 if not w in stop_words]
#
# def extract_human_tags(txt):
#     list1 = word_tokenize(txt)
#     return [w for w in list1 if not w in stop_words]
#
# def req_res_for_person(resume_id):
#
#     user_id = Resume.objects.filter(id=resume_id)
#
#
#     q1 = Resume.objects.all().values()
#     dfResumes = pd.DataFrame.from_records(q1)
#
#     q2 = User.objects.all().values()
#     dfUsers = pd.DataFrame.from_records(q2)
#     dfUsers = dfUsers.rename(index=str, columns={"id": "user_id"})
#
#     all_data = pd.merge(dfUsers, dfResumes, on='user_id', how='inner')
#
#
#
#     # ..........................................................................
#
#     # technical
#
#     to_process_users  = all_data[all_data['was_processed_x'] == 0]['user_id', 'skills']
#
#     for row in to_process_users.rows:
#         t = Users.objects.get(user_id=row['user_id'])
#         t.skills_processed = extract_technical_tags(row['skills'])
#         t.save()
#
#     to_process_resume = all_data[all_data['was_processed_y'] == 0]['id', 'text']
#
#     for row in to_process_resume.rows:
#         t = Users.objects.get(user_id=row['id'])
#         t.text_filtered = extract_human_tags(row['text'])
#         t.save()
#
#     # ..........................................................................
#
#     req_res(all_data)
#
#     # ..........................................................................
#
#     отрендерить ответ
# import nltk
#
# nltk.download()