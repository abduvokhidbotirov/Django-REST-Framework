from django.http import JsonResponse
import json
from rest_framework.generics import UpdateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Product
from .serializers import ProductSerializer


def api_home_(request):
    body = request.body
    data = {}
    try:
        data = json.loads(body)
    except:
        print('except')
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type
    data['params'] = request.GET
    return JsonResponse(data)


def api_home__(request):
    product = Product.objects.all().order_by('?').first()
    data = {}
    if product:
        data['id'] = product.id
        data['title'] = product.title
        data['content'] = product.content
        data['price'] = product.price

    return JsonResponse(data)


@api_view(['GET'])
def api_home(request):
    product = Product.objects.all()
    data = {}
    if product:
        data = ProductSerializer(product, many=True).data

    return Response(data)


@api_view(['POST'])
def api_post(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=201)
   # return Response({'detail': 'data not clean'})


@api_view(['GET'])
def api_detail(request, pk):
    instance = Product.objects.get(id=pk)
    serializer = ProductSerializer(instance)
    return Response(serializer.data, status=200)


@api_view(['PUT'])
def api_put(request, pk):
    instance = Product.objects.get(id=pk)
    serializer = ProductSerializer(data=request.data, instance=instance)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response({"detail": 'serializer is not valid'})


@api_view(['DELETE'])
def api_delete(request, pk):
    instance = Product.objects.get(id=pk)
    instance.delete()
    return Response(status=204)


@api_view(['GET', 'POST'])
def api_list_create(request):

    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, 200)

    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_rud(request, pk, *args, **kwargs):
    instance = Product.objects.get(id=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(instance)
        return Response(serializer.data, status=200)

    if request.method == 'PUT':
        serializer = ProductSerializer(instance=instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)

    if request.method == 'PATCH':
        partial = kwargs.pop('partial', False)
        serializer = ProductSerializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(status=502)

    if request.method == 'DELETE':
        instance.delete()
        return Response({'detail': 'Successfully deleted'}, status=204)
