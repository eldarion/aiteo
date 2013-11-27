from django.conf.urls import patterns, url


urlpatterns = patterns("aiteo.views",
    url(r"^$", "question_list", name="aiteo_question_list"),
    url(r"^ask/$", "question_create", name="aiteo_question_create"),
    url(r"^questions/(?P<pk>\d+)/$", "question_detail", name="aiteo_question_detail"),
    url(r"^questions/(?P<pk>\d+)/upvote/$", "question_upvote", name="aiteo_question_upvote"),
    url(r"^questions/(?P<pk>\d+)/downvote/$", "question_downvote", name="aiteo_question_downvote"),
    url(r"^responses/(?P<pk>\d+)/upvote/$", "response_upvote", name="aiteo_response_upvote"),
    url(r"^responses/(?P<pk>\d+)/downvote/$", "response_downvote", name="aiteo_response_downvote"),
    url(r"^responses/(?P<pk>\d+)/accept/$", "mark_accepted", name="aiteo_mark_accepted"),
)
