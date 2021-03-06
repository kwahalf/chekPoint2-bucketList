from flask_restplus import reqparse

pagination_and_search_arguments = reqparse.RequestParser()
pagination_and_search_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_and_search_arguments.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50, 100],
                                  default=10, help='Results per page {error_msg}')
pagination_and_search_arguments.add_argument('q')
