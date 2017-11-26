from .serializers import CustomerSerializer
from .models import Customer
from rest_framework import generics
import operator
from django.db.models import Q


class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetail(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        username = self.kwargs['username']
        return search(username)

def search(request):
    query = request
    print "Query: "+query
    if query:
        query_list = query.split()
        qset = (
            reduce(operator.and_,(Q(c_name__icontains=q) for q in query_list)) |
            reduce(operator.and_,(Q(c_address__icontains=q) for q in query_list)) |
            reduce(operator.and_,(Q(c_comment__icontains=q) for q in query_list))
        )
        results = Customer.objects.filter(qset)
    else:
        results = []
    print results
    return results