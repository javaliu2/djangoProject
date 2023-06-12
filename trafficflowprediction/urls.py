from django.urls import path

from trafficflowprediction.views import Upload, show, Update, Delete, Detail, Clean, Prediction, other, index

app_name = 'trafficflowprediction'

urlpatterns = [
    path('', index, name='index'),
    path('upload/', Upload.as_view(), name='upload'),
    path('show/<int:p>/', show, name='show'),
    path('<int:pk>/detail/', Detail.as_view(), name='detail'),
    path('<int:pk>/update/', Update.as_view(), name='update'),
    path('<int:pk>/delete/', Delete.as_view(), name='delete'),
    path('clean/', Clean.as_view(), name='clean'),
    path('prediction/', Prediction.as_view(), name='prediction'),
    path('other/', other, name='other'),
]
