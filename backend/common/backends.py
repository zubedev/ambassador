from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        res_data: OrderedDict = response.data

        res_data.update({  # insert current and last
            'current': self.page.number,
            'last': self.page.paginator.num_pages})

        res_data.move_to_end('last', last=False)  # move to the top
        res_data.move_to_end('current', last=False)  # move to the top

        return response
