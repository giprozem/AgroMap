from rest_framework.response import Response
from rest_framework.views import APIView
from ai.models import Contour_AI
from ai.productivity_funcs.predicting import productivity_predict
from indexes.models import PredictedContourVegIndex

# API view for predicting productivity based on vegetation index
class PredictingProductivityAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Filter PredictedContourVegIndex objects with specific index and date
        veg = PredictedContourVegIndex.objects.filter(index_id=1, date='2022-06-21')

        # Iterate through filtered objects and predict productivity
        for i in veg:
            # Predict productivity based on average_value from vegetation index
            result = productivity_predict(float(i.average_value))

            # Ensure the result is not negative
            if result <= 0:
                result = 0

            # Get the Contour_AI instance associated with the vegetation index
            contour = Contour_AI.objects.get(id=i.contour.id)

            # Update the productivity attribute of the Contour_AI instance
            contour.productivity = round(result, 3)

            # Save the updated Contour_AI instance
            contour.save()
            print(i.contour.id)

        return Response('ok', status=200)
