from django.urls import path 
from contact.views import contact_view, messages_view, message_read_view, message_public_view, message_detail_view, delete_contact_message_view


urlpatterns = [ 
    path('', contact_view, name="contact"),
    path('messages/', messages_view, name="contactmessages"),
    path('messages/detail/<int:id>', message_detail_view, name="contactmessagedetail"),
    path('messages/delete', delete_contact_message_view, name="deletecontactmessage"),
    path('messages/change-read/<int:id>', message_read_view, name="changemessageisread"),
    path('messages/change-public/<int:id>', message_public_view, name="changemessageispublic"),
]