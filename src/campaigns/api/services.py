from .models import Campaign
from .serializers import CampaignSerializer


class CampaignService:
    def get_info(self, account):
        campaingns = Campaign.objects.filter(account=account)
        serializer = CampaignSerializer(campaingns, many=True)
        return serializer.data
