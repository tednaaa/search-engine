from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Document
from .serializers import DocumentSerializer
from lib.query_completion import complete_query
from lib.custom_pagination import CustomPagination
from lib.query import run_query

@api_view(['GET'])
def get_suggestions(request):
    query = request.GET['query']

    completions = complete_query(query)
    return Response(completions)

@api_view(['GET'])
def search(request):
    query = request.GET['query']
    doc_ids = run_query(query)

    if not doc_ids:
        return Response(['No Results'])

    docs = [Document.objects.get(doc_id=doc_id) for doc_id in doc_ids]

    sorted_docs_by_count = sorted(docs, key=lambda d:d.views_count, reverse=True)

    paginator = CustomPagination()
    paginator.page_size = request.GET['page_size']
    result_page = paginator.paginate_queryset(sorted_docs_by_count, request)

    serializer_docs = DocumentSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer_docs.data)
