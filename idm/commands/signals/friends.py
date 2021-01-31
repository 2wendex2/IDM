from ...objects import dp, SignalEvent
from ...utils import new_message, edit_message
from vkapi import VkApiResponseException

@dp.signal_event_handle('подружиться')
def add_self_friend(event: SignalEvent) -> str:
    friend_id = event.msg['from_id']
    try:
        event.api('friends.add', user_id=friend_id)
        new_message(event.api, event.chat.peer_id,
            message="✅ Все отлично, запрос отправлен")
        return "ok"
    except VkApiResponseException as e:
        if e.error_code == 174:
            new_message(event.api, event.chat.peer_id,
            message="❗ Невозможно добавить в друзья самого себя")
        elif e.error_code == 175:
            new_message(event.api, event.chat.peer_id,
                message="❗ Невозможно добавить в друзья пользователя, который занес Вас в свой черный список")
        elif e.error_code == 176:
            new_message(event.api, event.chat.peer_id,
                message="❗ Невозможно добавить в друзья пользователя, который занесен в Ваш черный список")
        else:
            new_message(event.api, event.chat.peer_id,
                message=f"❗ Невозможно добавить в друзья пользователя: {e.error_msg}")
        return "ok"