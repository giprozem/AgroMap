from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# Custom pagination class for Contour model with a default page size of 100
class ContourPagination(PageNumberPagination):
    page_size = 100  # Set the default page size
    page_size_query_param = 'page_size'  # Define the query parameter to specify page size

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),  # Link to the next page of results
            'previous': self.get_previous_link(),  # Link to the previous page of results
            'count': self.page.paginator.count,  # Total number of objects across all pages
            'page_size': self.page_size,  # Current page size
            'results': data  # Actual data for the current page
        })

# Custom pagination class for CustomContour model with a default page size of 100
class CustomContourPagination(PageNumberPagination):
    page_size = 100  # Set the default page size
    page_size_query_param = 'page_size'  # Define the query parameter to specify page size

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),  # Link to the next page of results
            'previous': self.get_previous_link(),  # Link to the previous page of results
            'count': self.page.paginator.count,  # Total number of objects across all pages
            'page_size': self.page_size,  # Current page size
            'results': data  # Actual data for the current page
        })

# Custom pagination class for SearchContour model with a default page size of 20
class SearchContourPagination(PageNumberPagination):
    page_size = 20  # Set the default page size
    page_size_query_param = 'page_size'  # Define the query parameter to specify page size

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),  # Link to the next page of results
            'previous': self.get_previous_link(),  # Link to the previous page of results
            'count': self.page.paginator.count,  # Total number of objects across all pages
            'page_size': self.page_size,  # Current page size
            'results': data  # Actual data for the current page
        })
