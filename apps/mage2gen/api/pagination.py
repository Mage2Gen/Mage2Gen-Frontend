from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
	page_size = 100
	page_size_query_param = 'page_size'
	max_page_size = 1000


class LargeResultsSetPagination(PageNumberPagination):
	page_size = 5000
	page_size_query_param = 'page_size'
	max_page_size = 50000
