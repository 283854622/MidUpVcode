from django.conf.urls import url

from Myapp import views

urlpatterns = [
    url(r'^register/',views.register,name='register' ),
    url(r'^login/',views.login,name='login' ),
    url(r'^logout/',views.logout,name='logout' ),
    url(r'^mine/',views.mine,name='mine' ),
    url(r'^fuli/',views.fuli,name='fuli' ),
    url(r'^lottery/',views.lottery,name='lottery' ),
    url(r'^fuckoff/',views.fuckoff,name='fuckoff' ),


    url(r'^getvcode',views.getvcode,name='getvcode' ),

]
