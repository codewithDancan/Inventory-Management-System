from django.urls import path, register_converter, re_path
from django.views.generic import (TemplateView, RedirectView)
from .converters import YearConverter
from .views import (
    practice_view, practice_year_view, VehicleListView,
      VehicleDetailView, TestPageView, FormClassView,
        VehicleFormCreateView, VehicleModelFormCreateView,
          EngineCreateView, VehicleFormUpdateView, VehicleModelFormUpdateView,


          EngineViewSet,
            SellerViewSet,
              VehicleViewSet,
                VehicleModelViewSet,

                GetSellerView,
                GetSellerHTMLView,
                  GetSellerWithTokenView,

                  SellersView,
)
from rest_framework import routers



register_converter(YearConverter, 'year')


router = routers.DefaultRouter()
router.register(r"engines", EngineViewSet)
router.register(r"sellers", SellerViewSet)
router.register(r"vehicles", VehicleViewSet)
router.register(r"vehicle-models", VehicleModelViewSet)


urlpatterns = [
    path("get-seller/", GetSellerView.as_view(), name="get-seller"),
    path("seller/<int:id>/", GetSellerHTMLView.as_view(), name="seller-detail"),
    path("seller-token/<int:id>/", GetSellerWithTokenView.as_view(), name="seller-token-details"),
    path("all-sellers/", SellersView.as_view(), name="all-sellers"),






    path('my_year_path/<year:year>/', TemplateView.as_view(template_name='index.html'),
          kwargs={"sub_title": 'Backend Developer \n @ Space Ya Tech'}),
    re_path('app1/(?P<year>[0-9]{4})/$', TemplateView.as_view(template_name='index.html'),
          kwargs={"sub_title": 'Backend Developer \n @ Space Ya Tech'}),
    path('app1/unwanted_url/', RedirectView.as_view(url='http://localhost:8000/unwanted_url/')),
    path('my_year_path_2/<year:year>/', practice_view, name='year_url'),
    path('my_year_path_3/<year:year>/', practice_year_view),


    path('vehicle/', VehicleListView.as_view(), name='vehicle-view'),
    path('vehicle/<int:id>/', VehicleDetailView.as_view(), name='vehicle_detail_view'),
    

    path('form-class/', FormClassView.as_view()),
    path('form-class/contact-form-success/', TemplateView.as_view(template_name='contact-success.html'),
         kwargs= {
             'title': 'Form class View Success page',
             'page_id': 'form-class-success',
             'page_class': 'form-class-success-page',
             'h1_tag': 'This is the FormClassView success Page'
         }),

      path('vehicle-form-class/',VehicleFormCreateView.as_view(), name='vehicle-form-class'),
      path('vehicle-form-success/', TemplateView.as_view(template_name='vehicle-success.html'), name=' vehicle-form-success'),


      path('vehicle-model-form-class/',VehicleModelFormCreateView.as_view(), name='vehicle-model-form-class'),
      path('vehicle-model-form-success/', TemplateView.as_view(template_name='vehicle-model-form-success.html'), name=' vehicle-form-model-success'),


      path('engine-model-form-class/',EngineCreateView.as_view(), name='engine-model-form-class'),
      path('engine-model-form-success/', TemplateView.as_view(template_name='engine-form-success.html'), name=' engine-form-success'),

      path('vehicle-form-update-class/<int:id>/', VehicleFormUpdateView.as_view(), name='vehicle-form-update'),
      path('vehicle-model-form-update-class/<int:id>/', VehicleModelFormUpdateView.as_view(), name='vehicle-model-form-update'),

      
]
