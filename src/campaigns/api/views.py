import requests

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from .models import Campaign
from .serializers import CampaignSerializer
from .services import CampaignService


@renderer_classes(JSONRenderer)
@api_view(['GET'])
def get_campaigns(request, account):
    campaigns = CampaignService().get_info(account=account)
    return Response(
        status=status.HTTP_200_OK,
        data=campaigns
    )
