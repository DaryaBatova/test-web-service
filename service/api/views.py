from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from .models import Page
from .serializers import PageSerializer
from .process_url import process_url


class InvalidRequestParamsException(APIException):
    status_code = 400
    default_detail = 'Invalid parameters.'
    default_code = 'bad_params'


@api_view(['GET', 'HEAD'])
def page_detail(request, pk):
    """
    The detailed information for the loaded page.
    """
    try:
        page = Page.objects.get(pk=pk)
    except Page.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PageSerializer(page)
    return Response(serializer.data)


@api_view(['POST', 'HEAD'])
def page_create(request):
    """
    Create the detailed information of a page.
    """
    url = request.data.get('url', None)
    if url is None:
        # bad params
        raise InvalidRequestParamsException(f'Invalid parameters: {dict(request.data)}. '
                                            f'Expected: {dict(url="some_url")}')
    detail_page = process_url(url)
    if detail_page is False:
        # problems with connection
        raise InvalidRequestParamsException(f'An error occurred while trying to establish a connection with {url}')
    if Page.objects.filter(url=url).exists():
        page = Page.objects.get(url=url)
        serializer = PageSerializer(page, data=detail_page)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        serializer = PageSerializer(data=detail_page)
        if serializer.is_valid():
            page = serializer.save()
            page.url = url
            page.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
