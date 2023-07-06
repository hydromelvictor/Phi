#!/usr/bin/env python3
# """ chats collections """
# from . import chats, sms
# from datetime import datetime
# from uuid import uuid4

# def chats_save(users, msg):
#     """ chat """
    
#     chats.insert_one(
#         {
#             '_id': str(uuid4()),
#             'publish': datetime.utcnow(),
#             'users': users,
#             'sms': sms.find({''})
#         }
#     )

# def sms_save(chat_id, sender, text, publish, reciever):
#     """ message in chat """
#     sms.insert_one()