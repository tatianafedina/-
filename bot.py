from configparser import ConfigParser
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

from object import Dialog
from storage import get_dialog, store_dialog

DIALOG_STATE_WAIT_COURSE = 'wait_course'


def process_event(vk, event):
    dialog = get_dialog(event.user_id)
    if dialog is None:
        dialog = Dialog()
        dialog.user_id = event.user_id
        dialog.state = DIALOG_STATE_WAIT_COURSE
        store_dialog(dialog)
        send_enter_course_message(vk, dialog.user_id)
        return
    if dialog.state == DIALOG_STATE_WAIT_COURSE:
        text = event.text
        if not text.isdigit():
            send_enter_course_message(vk, dialog.user_id)
            return
        course = int(text)
        dialog.course = course
        dialog.state = None
        store_dialog(dialog)
        return
    if not dialog or dialog.state is None:
        pass  # Обработка сообщений может быть здесь


def send_enter_course_message(vk, user_id):
    vk.messages.send(user_id=user_id, message='Для продолжения необходимо знать ваш курс.\n\n'
                                              'Введите номер вашего курса')


def send_course_success_message(vk, user_id):
    vk.messages.send(user_id=user_id, message='Курс сохранен')


if __name__ == '__main__':

    config = ConfigParser()
    config.read('config.ini')

    vk_session = VkApi(token=config.get('VK', 'token'))

    vk = vk_session.get_api()

    poll = VkLongPoll(vk_session)

    for event in poll.listen():
        print(event.type)
        if event.type != VkEventType.MESSAGE_NEW or not event.to_me:
            continue

        print(event)

        # Пустой текст
        if not event.text:
            continue

        process_event(vk, event)

