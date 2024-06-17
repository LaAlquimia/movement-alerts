import requests

def enviar_mensaje_html(bot_token, chat_id, html_message):
    """
    Envía un mensaje HTML a un chat de Telegram.

    :param bot_token: Token del bot de Telegram.
    :param chat_id: ID del chat de Telegram.
    :param html_message: Mensaje HTML a enviar.
    :return: None
    """
    # URL de la API de Telegram para enviar mensajes
    send_message_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    # Parámetros para la solicitud
    params = {
        'chat_id': chat_id,
        'text': html_message,
        'parse_mode': 'HTML'
    }
    # Realiza la solicitud POST para enviar el mensaje
    response = requests.post(send_message_url, data=params, timeout=100)
    # Verifica la respuesta
    if response.status_code == 200:
        print("Mensaje enviado exitosamente")
    else:
        print("Error al enviar el mensaje:", response.text)
