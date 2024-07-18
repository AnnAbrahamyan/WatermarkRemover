import asyncio
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Image
from .serializers import ImageSerializer
from pixelbin import PixelbinClient, PixelbinConfig
from pixelbin.utils.url import obj_to_url


config = PixelbinConfig({
    "domain": "https://api.pixelbin.io",
    "apiSecret": "d9bfa4d9-2ef9-4c76-9573-888f3bf091fa",
})

pixelbin = PixelbinClient(config=config)


class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():

            image = serializer.validated_data['image']
            
            image_stream = image.read()

            try:
                result = asyncio.run(pixelbin.assets.fileUploadAsync(
                    file=image_stream,
                    name="watermarkremover.jpeg",
                    tags=["watermark"],
                    metadata={},
                    overwrite=False,
                    filenameOverride=True))


                obj = {
                    "cloudName": "watermark_remover_smartcode",
                    "version": "v2",
                    "transformations": [{"name":"remove","plugin":"wm"}],
                    "filePath": result['name'],
                    "baseUrl": "https://cdn.pixelbin.io",
                }

                url = obj_to_url(obj)


                return Response({'url': url}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        









#    createSignedUrlV2Async     