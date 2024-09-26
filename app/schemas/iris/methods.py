import enum


class IrisDutyEventMethod(enum.Enum):
    """Методы для обработки событий."""

    ADD_USER = "addUser"
    BAN_EXPIRED = "banExpired"
    BAN_GET_REASON = "banGetReason"
    BIND_CHAT = "bindChat"
    DELETE_MESSAGES_FROM_USER = "deleteMessagesFromUser"
    DELETE_MESSAGES = "deleteMessages"
    FORBIDDEN_LINKS = "forbiddenLinks"
    PING = "ping"
    PRINT_BOOKMARK = "printBookmark"
    SUBSCRIBE_SIGNALS = "subscribeSignals"
    TO_GROUP = "toGroup"
    SEND_SIGNAL = "sendSignal"
    SEND_MY_SIGNAL = "sendMySignal"
    HIRE_API = "hireApi"
    MEET_CHAT_DUTY = "meetChatDuty"
    MESSAGES_DELETE_BY_TYPE = "messages.deleteByType"
    GROUP_BOTS_INVITED = "groupbots.invited"
    MESSAGES_RECOGNISE_AUDIO_MESSAGE = "messages.recogniseAudioMessage"
