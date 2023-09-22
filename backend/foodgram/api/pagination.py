from rest_framework.pagination import PageNumberPagination

import constants


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = constants.PAGE_SIZE
