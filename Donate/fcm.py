from pyfcm import FCMNotification
import environ

env = environ.Env()
environ.Env.read_env()


def send_push_notification(
    title="",
    body="",
    data_message={},
    registration_id="",
    user_id=0,
    child_id=0,
    notification_type="",
):
    
    fcm = FCMNotification(
        service_account_file="<service-account-json-path>", project_id="<project-id>")

    # push_service = FCMNotification(
    #     api_key=env("FCM_SERVER_KEY").replace("'", ""))

    # Notification.objects.create(
    #     title=title,
    #     description=body,
    #     user_id=user_id,
    #     child_id=child_id,
    #     type=notification_type,
    # )

    # result = push_service.notify_single_device(
    #     registration_id=registration_id,
    #     message_title=title,
    #     message_body=body,
    #     data_message=data_message,
    # )
    # print('resulrrrr',result)


def send_push_notification_multiple_devices(
    title="", body="", data_message={}, registration_ids=[]
):
    push_service = FCMNotification(
        api_key=env("FCM_SERVER_KEY").replace("'", ""))
    result = push_service.notify_multiple_devices(
        registration_ids=registration_ids,
        message_title=title,
        message_body=body,
        data_message=data_message,
    )
