from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)

from users.models import User


def q_search(query):

    vector = SearchVector('username', 'last_name', 'about_me',)
    query = SearchQuery(query)

    return User.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")
