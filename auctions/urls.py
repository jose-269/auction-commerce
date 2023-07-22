from django.urls import path
from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("newList/", views.newList, name="newList"),
    path("listing/<int:id>", views.listing_view, name="listing"),
    path('watchlists/', views.watchinglists_view, name="watchlists"),
    path('watchlist/add/<int:listing_id>' ,views.add_watchinglist, name="add_watchinglist"),
    path('watchlist/remove/<int:listing_id>' ,views.remove_watchinglist, name="remove_watchinglist"),
    path('place-a-bid/<int:listing_id>', views.place_a_bid, name="place_a_bid"),
    path('close-bid/<int:listing_id>', views.close_bid, name="close_bid"),
    path('won-listings/', views.won_listings, name="won_listings"),
    path('comments/<int:listing_id>', views.add_comment, name="add_comment"),
    path('categories/', views.categories_view, name="categories"),
    # path('<path:not_found>/', views.error_404_view, name='error_404'),
]
