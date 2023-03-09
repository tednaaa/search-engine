from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Document
from .serializers import DocumentSerializer
from lib.query_completion import complete_query
from lib.query import run_query

@api_view(['GET'])
def complete(request):
    query = request.GET['q']

    completions = complete_query(query)
    return Response(completions)

@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]

    return Response(routes)

@api_view(['GET'])
def get_docs(request):
    query = request.GET['query']
    doc_ids = run_query(query)

    if not doc_ids:
        return Response(['No Results'])

    docs = [Document.objects.get(doc_id=doc_id) for doc_id in doc_ids]

    sorted_docs_by_count = sorted(docs, key=lambda d:d.views_count, reverse=True)

    serializer_docs = DocumentSerializer(sorted_docs_by_count, many=True)

    return Response(serializer_docs.data)
