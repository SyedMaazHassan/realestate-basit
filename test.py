from django.contrib import admin
from .models import Ticket,TicketResponse
# Register your models here.

class ResponseInline(admin.TabularInline):
    model = TicketResponse
    extra = 1
    can_delete = False
    can_add = True
    can_edit = False
    readonly_fields = fields = ("message", "sent_from", "created_at")

class TicketAdmin(admin.ModelAdmin):
    model = Ticket
    inlines = [ResponseInline] 
    list_display = [ "title", "status", "created_at","created_by"]
    search_fields = ["title"]


admin.site.register(Ticket,TicketAdmin)


####
from django.db import models
from authentication.models import User
# Create your models here.
class TicketStatus(models.TextChoices):
    OPEN = "Open"
    AWAITING_YOUR_REPLY = "Awaiting your reply"
    SOLVED = 'Solved'

class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    assignee = models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(max_length=25, choices=TicketStatus.choices, default=TicketStatus.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class TicketResponse(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    message = models.TextField()
    sent_from = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ("-created_at",)
###
from rest_framework import serializers
from .models import Ticket,TicketResponse


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        
class TicketResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketResponse
        fields = "__all__"

##
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('tickets', TicketView, basename='tickets')

urlpatterns = [
    path("", include(router.urls)),
]

##
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import TicketSerializer,TicketResponseSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Ticket,TicketResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

# Create your views here.
class TicketView(ModelViewSet):
    queryset = Ticket.objects.all()
    http_method_names = ['get','post']
    permission_classes = [IsAuthenticated,]
    error_status = status.HTTP_400_BAD_REQUEST
    output_data_for_error = {"message": None}

    def list(self,request):
        tickets = self.queryset.filter(created_by=request.user)
        serializer = TicketSerializer(tickets,many=True)
        return Response(serializer.data)

    def retrieve(self, request,pk):
        ticket = Ticket.objects.filter(pk=pk).first()
        if not ticket:
            self.output_data_for_error['message'] = "Invalid Primary Key"
            return Response(self.output_data_for_error, self.error_status)
        if ticket.created_by != request.user:
            self.output_data_for_error['message'] = "You did not create this ticket"
            return Response(self.output_data_for_error, self.error_status)
        
        responses = TicketResponse.objects.filter(ticket=ticket)
        print(responses)
        serializer = TicketResponseSerializer(responses,many=True)
        
        return Response(serializer.data)

    

    def create(self,request):
        title = request.data.get("title")

        if not title:
            self.output_data_for_error['message'] = "You must provide a title for the ticket"
            return Response(self.output_data_for_error, self.error_status)

        # Checking if the current user already has 10 open tickets
        if len(Ticket.objects.filter(created_by=request.user,status="Open")) >=10:
            self.output_data_for_error['message'] = "You already have 10 open tickets so can not create anymore"
            return Response(self.output_data_for_error, self.error_status)

        ticket = Ticket.objects.create(title=title,created_by=request.user)
        ticket.save()
        serializer=TicketSerializer(ticket)
        return Response(serializer.data)


    @action(detail=True, methods=['post'])
    def response(self,request,pk):
        message = request.data.get("message")
        if not message:
            self.output_data_for_error['message'] = "You must provide a message"
            return Response(self.output_data_for_error, self.error_status)

        ticket = Ticket.objects.filter(id=pk).first()

        if not ticket:
            self.output_data_for_error['message'] = "Invalid Primary Key"
            return Response(self.output_data_for_error, self.error_status)
        
        if ticket.status == "Solved":
            self.output_data_for_error['message'] = "The status of this ticket is solved so you can not sent a response."
            return Response(self.output_data_for_error, self.error_status)

        if ticket.created_by != request.user:
            self.output_data_for_error['message'] = "You did not create this ticket"
            return Response(self.output_data_for_error, self.error_status)

        ticket_response = TicketResponse.objects.create(ticket=ticket,message=message,sent_from=request.user)
        ticket_response.save()
        return Response({"message":"Response sent successfully."})