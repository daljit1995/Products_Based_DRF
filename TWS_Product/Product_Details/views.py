from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Product_Details.serializers import ProductSerializer
from Product_Details.models import Product
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count



class Product_API(APIView):

    def post(self, request, pk=None):

        data_=request.data
        serializer_data=ProductSerializer(data=data_)

        title = data_.get('title')
        description = data_.get('description')
        price = data_.get('price')

        data_['created_date'] = timezone.now()
        data_['updated_date'] = timezone.now()

        try:
            product = Product.objects.get(title=title, description=description, price=price)
            product.retrieval_counts += 1
            product.updated_date = timezone.now()
            product.save()

            return Response({'Message':'Submitted Successfully!'}, status=status.HTTP_200_OK)
        except:
            serializer_data = ProductSerializer(data = data_)
            if serializer_data.is_valid():
                serializer_data.save()
                return Response({'Message':'Submitted Successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response({'Message':'Enter the Valid Input!'}, status=status.HTTP_400_BAD_REQUEST) 
        
    def get(self,request,pk=None):
        
        try:
            if pk is not None:
                products_detail = Product.objects.get(id=pk)
                if products_detail is not None:
                    data_serializer = ProductSerializer(products_detail)
                    
                    return Response(data_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"Message":"Record Not Found!"}, status=status.HTTP_404_NOT_FOUND)
            else:
                try:
                    products_detail = Product.objects.all()
                except:
                    return Response({"Message":"Please Enter the Valid Input!"}, status=status.HTTP_400_BAD_REQUEST)
                
                if products_detail:
                    data_serializer = ProductSerializer(products_detail, many=True)
                    return Response(data_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"Message":"Record Not Found!"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"Message":"Please Enter Valid Input!"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            data_verification = Product.objects.get(id = pk)
        except:
            return Response({"Message":"Record Not Found!"}, status=status.HTTP_404_NOT_FOUND)
        
        data_ = request.data
        data_['updated_date'] = timezone.now()

        data_serializer = ProductSerializer(data_verification, data=data_, partial=True)
        if data_serializer.is_valid():
            data_serializer.save()
            return Response({"Message":"Updated Successfully!"})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        
        try:
            data_delete = Product.objects.get(id = pk)
        except:
            return Response({"Message":"Record Not Found!"}, status=status.HTTP_404_NOT_FOUND)   

        data_delete.delete()
        return Response({"Message":"Data Deleted!"}, status=status.HTTP_204_NO_CONTENT) 

class Data_presentation(APIView):

    def get(self, request):
        
        products = Product.objects.filter(retrieval_counts__gt=0).order_by('-retrieval_counts')[:5]
        product_last_day = Product.objects.filter(retrieval_counts__gt=0, created_date__gte=timezone.now() - timedelta(days=1)).order_by('-retrieval_counts')[:5]
        product_last_week = Product.objects.filter(retrieval_counts__gt=0, created_date__gte=timezone.now() - timedelta(weeks=1)).order_by('-retrieval_counts')[:5]
        
        serializer1 = ProductSerializer(products, many=True)
        serializer2 = ProductSerializer(product_last_day, many=True)
        serializer3 = ProductSerializer(product_last_week, many=True)
     
        return Response({"All Top 5": serializer1.data, "Last Day Top 5": serializer2.data, "Last Week Top 5": serializer3.data})