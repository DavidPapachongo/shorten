from typing import Counter
from django.conf import urls
from django.db.models.expressions import OrderBy, Value
from django.db.models.query_utils import Q
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from shortURL.serializers import UrlSerializer, ClickSerializer
from shortURL.models import UrlModel, ClickModel
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status, generics
from django.http import Http404, HttpResponseRedirect
from django.db.models import Count
from baseconv import  base62

class Link(APIView):
    
    def get(self, request, format=None):
        links = UrlModel.objects.all()
        serializer = UrlSerializer(links, many=True)
        return JsonResponse(serializer.data, safe=False)


    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = UrlSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class LinkDetail(APIView):

    def get_object(self, pk):
        try:
            return UrlModel.objects.annotate(clicks_counter=Count('clickmodel')).get(pk=pk)
        except UrlModel.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        link = self.get_object(pk)
        serializer = UrlSerializer(link)
        return JsonResponse(serializer.data)
        

    def put(self, request, pk, format=None):
        link = self.get_object(pk)
        serializer = UrlSerializer(link, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


    def delete(self, request, pk, format=None):
        link = self.get_object(pk)
        link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def redirect_link(request, pk):
    try:
        pk = base62.decode(pk)
        pk = int(pk)
        url = UrlModel.objects.get(pk=pk)
        user_agent = request.META.get('HTTP_USER_AGENT', None)
        ClickModel.objects.create(url = url, user_agent = user_agent)
        return HttpResponseRedirect(url.link)
    except UrlModel.DoesNotExist:
        raise Http404

class Clicks(APIView):
    def get(self, request, format=None):
        clicks = ClickModel.objects.all()       
        serializer = ClickSerializer(clicks, many=True)
        return JsonResponse(serializer.data, safe=False)


class LinkClicks(APIView):
    def get(self, request, format=None):
        queryset = ClickModel.objects.all()
        link = request.query_params.get('link_id')
        if link is not None:
            queryset = queryset.filter( url_id = link)
            serializer = ClickSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
        