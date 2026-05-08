from django.http import FileResponse, Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views import View
from .models import Download
from django.utils import timezone
import os

class SecureDownloadView(View):
    def get(self, request, token):
        download = get_object_or_404(Download, token=token)

        # Security Rule: Only the buyer who purchased can access
        if download.order.buyer != request.user:
            return HttpResponseForbidden("You do not have access to this download.")

        # Security Rule: Download tokens expire after 24 hours
        if download.is_expired():
            return HttpResponseForbidden("This download link has expired.")

        product_file = download.order.product.product_file
        if not product_file:
            raise Http404("File not found.")

        # Optional: Mark as downloaded
        download.downloaded = True
        download.save()

        response = FileResponse(product_file.open('rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(product_file.name)}"'
        return response
