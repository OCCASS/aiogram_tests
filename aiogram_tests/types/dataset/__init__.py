from aiogram import types

from .base import DatasetItem

USER = DatasetItem(
    {
        "id": 12345678,
        "is_bot": False,
        "first_name": "FirstName",
        "last_name": "LastName",
        "username": "username",
        "language_code": "ru",
    },
    model=types.User,
)

CHAT = DatasetItem(
    {
        "id": 12345678,
        "first_name": "FirstName",
        "last_name": "LastName",
        "username": "username",
        "type": "private",
    },
    model=types.Chat,
)

CHAT_PHOTO = DatasetItem(
    {
        "small_file_id": "small_file_id",
        "small_file_unique_id": "small_file_unique_id",
        "big_file_id": "big_file_id",
        "big_file_unique_id": "big_file_unique_id",
    },
    model=types.ChatPhoto,
)

PHOTO = DatasetItem(
    {
        "file_id": "AgADBAADFak0G88YZAf8OAug7bHyS9x2ZxkABHVfpJywcloRAAGAAQABAg",
        "file_unique_id": "file_unique_id",
        "file_size": 1101,
        "width": 90,
        "height": 51,
    },
    model=types.PhotoSize,
)

AUDIO = DatasetItem(
    {
        "duration": 236,
        "mime_type": "audio/mpeg3",
        "title": "The Best Song",
        "performer": "The Best Singer",
        "file_id": "CQADAgADbQEAAsnrIUpNoRRNsH7_hAI",
        "file_size": 9507774,
        "file_unique_id": "file_unique_id",
    },
    model=types.Audio,
)

BOT_COMMAND = DatasetItem(
    {
        "command": "start",
        "description": "Start bot",
    },
    model=types.BotCommand,
)

CHAT_MEMBER = DatasetItem(
    {
        "user": USER,
        "status": "administrator",
        "can_be_edited": False,
        "can_manage_chat": True,
        "can_change_info": True,
        "can_delete_messages": True,
        "can_invite_users": True,
        "can_restrict_members": True,
        "can_pin_messages": True,
        "can_promote_members": False,
        "can_manage_voice_chats": True,  # Deprecated
        "can_manage_video_chats": True,
        "is_anonymous": False,
    },
    model=types.ChatMember,
)

CHAT_MEMBER_OWNER = DatasetItem(
    {
        "user": USER,
        "status": "creator",
        "is_anonymous": False,
    },
    model=types.ChatMemberOwner,
)

CONTACT = DatasetItem(
    {
        "phone_number": "88005553535",
        "first_name": "John",
        "last_name": "Smith",
    },
    model=types.Contact,
)

DICE = DatasetItem({"value": 6, "emoji": "🎲"}, model=types.Dice)

DOCUMENT = DatasetItem(
    {
        "file_name": "test.docx",
        "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "file_id": "BQADAgADpgADy_JxS66XQTBRHFleAg",
        "file_unique_id": "file_unique_id",
        "file_size": 21331,
    },
    model=types.Document,
)

ANIMATION = DatasetItem(
    {
        "file_id": "file_id",
        "file_unique_id": "file_unique_id",
        "width": 50,
        "height": 50,
        "duration": 50,
    },
    model=types.Animation,
)

ENTITY_BOLD = DatasetItem(
    {
        "offset": 5,
        "length": 2,
        "type": "bold",
    }
)

ENTITY_ITALIC = DatasetItem(
    {
        "offset": 8,
        "length": 1,
        "type": "italic",
    }
)

ENTITY_LINK = DatasetItem(
    {
        "offset": 10,
        "length": 6,
        "type": "text_link",
        "url": "https://google.com/",
    }
)

ENTITY_CODE = DatasetItem(
    {
        "offset": 17,
        "length": 7,
        "type": "code",
    }
)

ENTITY_PRE = DatasetItem(
    {
        "offset": 30,
        "length": 4,
        "type": "pre",
    }
)

ENTITY_MENTION = DatasetItem(
    {
        "offset": 47,
        "length": 9,
        "type": "mention",
    }
)

GAME = DatasetItem(
    {
        "title": "Karate Kido",
        "description": "No trees were harmed in the making of this game :)",
        "photo": [PHOTO, PHOTO, PHOTO],
        "animation": ANIMATION,
    },
    model=types.Game,
)

INVOICE = DatasetItem(
    {
        "title": "Working Time Machine",
        "description": "Want to visit your great-great-great-grandparents? "
        "Make a fortune at the races? "
        "Shake hands with Hammurabi and take a stroll in the Hanging Gardens? "
        "Order our Working Time Machine today!",
        "start_parameter": "time-machine-example",
        "currency": "USD",
        "total_amount": 6250,
    },
    model=types.Invoice,
)

LOCATION = DatasetItem(
    {
        "latitude": 50.693416,
        "longitude": 30.624605,
    },
    model=types.Location,
)

VENUE = DatasetItem(
    {
        "location": LOCATION,
        "title": "Venue Name",
        "address": "Venue Address",
        "foursquare_id": "4e6f2cec483bad563d150f98",
    },
    model=types.Venue,
)

SHIPPING_ADDRESS = DatasetItem(
    {
        "country_code": "US",
        "state": "State",
        "city": "DefaultCity",
        "street_line1": "Central",
        "street_line2": "Middle",
        "post_code": "424242",
    },
    model=types.ShippingAddress,
)

STICKER = DatasetItem(
    {
        "width": 512,
        "height": 512,
        "emoji": "🛠",
        "set_name": "StickerSet",
        "thumb": PHOTO,
        "file_id": "AAbbCCddEEffGGhh1234567890",
        "file_size": 12345,
        "file_unique_id": "file_unique_id",
        "type": "type",
        "is_animated": False,
        "is_video": False,
    },
    model=types.Sticker,
)

SUCCESSFUL_PAYMENT = DatasetItem(
    {
        "currency": "USD",
        "total_amount": 6250,
        "invoice_payload": "HAPPY FRIDAYS COUPON",
        "telegram_payment_charge_id": "_",
        "provider_payment_charge_id": "12345678901234_test",
    },
    model=types.SuccessfulPayment,
)

VIDEO = DatasetItem(
    {
        "duration": 52,
        "width": 853,
        "height": 480,
        "mime_type": "video/quicktime",
        "thumb": PHOTO,
        "file_id": "BAADAgpAADdawy_JxS72kRvV3cortAg",
        "file_unique_id": "file_unique_id",
        "file_size": 10099782,
    },
    model=types.Video,
)

VIDEO_NOTE = DatasetItem(
    {
        "duration": 4,
        "length": 240,
        "thumb": PHOTO,
        "file_id": "AbCdEfGhIjKlMnOpQrStUvWxYz",
        "file_unique_id": "file_unique_id",
        "file_size": 186562,
    },
    model=types.VideoNote,
)

VOICE = DatasetItem(
    {
        "duration": 1,
        "mime_type": "audio/ogg",
        "file_id": "AwADawAgADADy_JxS2gopIVIIxlhAg",
        "file_unique_id": "file_unique_id",
        "file_size": 4321,
    },
    model=types.Voice,
)

CALLBACK_QUERY = DatasetItem(
    {
        "id": "12345678",
        "chat_instance": "AABBCC",
        "from": USER,
        "chat": CHAT,
        "data": "data",
    },
    model=types.CallbackQuery,
)

CHANNEL = DatasetItem(
    {
        "type": "channel",
        "username": "best_channel_ever",
        "id": -1001065170817,
    },
    model=types.Chat,
)

CHANNEL_POST = DatasetItem(
    {
        "message_id": 12345,
        "sender_chat": CHANNEL,
        "chat": CHANNEL,
        "date": 1508825372,
        "text": "Hi, channel!",
    },
    model=types.Message,
)

EDITED_CHANNEL_POST = DatasetItem(
    {
        "message_id": 12345,
        "sender_chat": CHANNEL,
        "chat": CHANNEL,
        "date": 1508825372,
        "edit_date": 1508825379,
        "text": "Hi, channel! (edited)",
    },
    model=types.Message,
)

EDITED_MESSAGE = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508825372,
        "edit_date": 1508825379,
        "text": "hi there (edited)",
    },
    model=types.Message,
)

FORWARDED_MESSAGE = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1522828529,
        "forward_from_chat": CHAT,
        "forward_from_message_id": 123,
        "forward_date": 1522749037,
        "text": "Forwarded text with entities from public channel ",
        "entities": [
            ENTITY_BOLD,
            ENTITY_CODE,
            ENTITY_ITALIC,
            ENTITY_LINK,
            ENTITY_LINK,
            ENTITY_MENTION,
            ENTITY_PRE,
        ],
    },
    model=types.Message,
)

MESSAGE = DatasetItem(
    {
        "message_id": 11223,
        "from": USER,
        "chat": CHAT,
        "date": 1508709711,
        "text": "Hi, world!",
    },
    model=types.Message,
)

MESSAGE_WITH_AUDIO = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508739776,
        "audio": AUDIO,
        "caption": "This is my favourite song",
    },
    model=types.Message,
)

MESSAGE_WITH_CONTACT = DatasetItem(
    {
        "message_id": 56006,
        "from": USER,
        "chat": CHAT,
        "date": 1522850298,
        "contact": CONTACT,
    },
    model=types.Message,
)

MESSAGE_WITH_DICE = DatasetItem(
    {"message_id": 12345, "from": USER, "chat": CHAT, "date": 1508768012, "dice": DICE},
    model=types.Message,
)

MESSAGE_WITH_DOCUMENT = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508768012,
        "document": DOCUMENT,
        "caption": "Read my document",
    },
    model=types.Message,
)

MESSAGE_WITH_GAME = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508824810,
        "game": GAME,
    },
    model=types.Message,
)

MESSAGE_WITH_INVOICE = DatasetItem(
    {
        "message_id": 9772,
        "from": USER,
        "chat": CHAT,
        "date": 1508761719,
        "invoice": INVOICE,
    },
    model=types.Message,
)

MESSAGE_WITH_LOCATION = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508755473,
        "location": LOCATION,
    },
    model=types.Message,
)

MESSAGE_WITH_MIGRATE_TO_CHAT_ID = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1526943253,
        "migrate_to_chat_id": -1234567890987,
    },
    model=types.Message,
)

MESSAGE_WITH_MIGRATE_FROM_CHAT_ID = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1526943253,
        "migrate_from_chat_id": -123456789,
    },
    model=types.Message,
)

MESSAGE_WITH_PHOTO = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508825154,
        "photo": [PHOTO, PHOTO, PHOTO, PHOTO],
        "caption": "photo description",
    },
    model=types.Message,
)

MESSAGE_WITH_MEDIA_GROUP = DatasetItem(
    {
        "message_id": 55966,
        "from": USER,
        "chat": CHAT,
        "date": 1522843665,
        "media_group_id": "12182749320567362",
        "photo": [PHOTO, PHOTO, PHOTO, PHOTO],
    },
    model=types.Message,
)

MESSAGE_WITH_STICKER = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508771450,
        "sticker": STICKER,
    },
    model=types.Message,
)

MESSAGE_WITH_SUCCESSFUL_PAYMENT = DatasetItem(
    {
        "message_id": 9768,
        "from": USER,
        "chat": CHAT,
        "date": 1508761169,
        "successful_payment": SUCCESSFUL_PAYMENT,
    },
    model=types.Message,
)

MESSAGE_WITH_VENUE = DatasetItem(
    {
        "message_id": 56004,
        "from": USER,
        "chat": CHAT,
        "date": 1522849819,
        "location": LOCATION,
        "venue": VENUE,
    },
    model=types.Message,
)

MESSAGE_WITH_VIDEO = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508756494,
        "video": VIDEO,
        "caption": "description",
    },
    model=types.Message,
)

MESSAGE_WITH_VIDEO_NOTE = DatasetItem(
    {
        "message_id": 55934,
        "from": USER,
        "chat": CHAT,
        "date": 1522835890,
        "video_note": VIDEO_NOTE,
    },
    model=types.Message,
)

MESSAGE_WITH_VOICE = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508768403,
        "voice": VOICE,
    },
    model=types.Message,
)

MESSAGE_FROM_CHANNEL = DatasetItem(
    {
        "message_id": 123432,
        "from": None,
        "chat": CHANNEL,
        "date": 1508768405,
        "text": "Hi, world!",
    },
    model=types.Message,
)

PRE_CHECKOUT_QUERY = DatasetItem(
    {
        "id": "262181558630368727",
        "from": USER,
        "currency": "USD",
        "total_amount": 6250,
        "invoice_payload": "HAPPY FRIDAYS COUPON",
    },
    model=types.PreCheckoutQuery,
)

REPLY_MESSAGE = DatasetItem(
    {
        "message_id": 12345,
        "from": USER,
        "chat": CHAT,
        "date": 1508751866,
        "reply_to_message": MESSAGE,
        "text": "Reply to quoted message",
    },
    model=types.Message,
)

SHIPPING_QUERY = DatasetItem(
    {
        "id": "262181558684397422",
        "from": USER,
        "invoice_payload": "HAPPY FRIDAYS COUPON",
        "shipping_address": SHIPPING_ADDRESS,
    },
    model=types.ShippingQuery,
)

USER_PROFILE_PHOTOS = DatasetItem(
    {
        "total_count": 1,
        "photos": [
            [PHOTO, PHOTO, PHOTO],
        ],
    },
    model=types.UserProfilePhotos,
)

FILE = DatasetItem(
    {
        "file_id": "XXXYYYZZZ",
        "file_size": 5254,
        "file_path": "voice/file_8",
        "file_unique_id": "file_unique_id",
    },
    model=types.File,
)

UPDATE = DatasetItem(
    {
        "update_id": 123456789,
        "message": MESSAGE,
    },
    model=types.Update,
)

WEBHOOK_INFO = DatasetItem(
    {
        "url": "",
        "has_custom_certificate": False,
        "pending_update_count": 0,
    },
    model=types.WebhookInfo,
)

REPLY_KEYBOARD_MARKUP = DatasetItem(
    {
        "keyboard": [[{"text": "something here"}]],
        "resize_keyboard": True,
    },
    model=types.ReplyKeyboardMarkup,
)

CHAT_PERMISSIONS = DatasetItem(
    {
        "can_send_messages": True,
        "can_send_media_messages": True,
        "can_send_polls": True,
        "can_send_other_messages": True,
        "can_add_web_page_previews": True,
        "can_change_info": True,
        "can_invite_users": True,
        "can_pin_messages": True,
    },
    model=types.ChatPermissions,
)

CHAT_LOCATION = DatasetItem(
    {
        "location": LOCATION,
        "address": "address",
    },
    model=types.ChatLocation,
)

FULL_CHAT = DatasetItem(
    {
        **CHAT,
        "photo": CHAT_PHOTO,
        "bio": "bio",
        "has_private_forwards": False,
        "description": "description",
        "invite_link": "invite_link",
        "pinned_message": MESSAGE,
        "permissions": CHAT_PERMISSIONS,
        "slow_mode_delay": 10,
        "message_auto_delete_time": 60,
        "has_protected_content": True,
        "sticker_set_name": "sticker_set_name",
        "can_set_sticker_set": True,
        "linked_chat_id": -1234567890,
        "location": CHAT_LOCATION,
    },
    model=types.Chat,
)
