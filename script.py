import time
from binance.client import Client
from config import *
from message import enviar_mensaje_html

client = Client('','', tld='com')

def buscarticks():
    ticks = []
    lista_ticks = client.futures_symbol_ticker() # traer todas las monedas de futuros de binace
    print('Numero de monedas encontradas #' + str(len(lista_ticks)))

    for tick in lista_ticks:
        if tick['symbol'][-4:] != 'USDT': # seleccionar todas las monedas en el par USDT
            continue
        ticks.append(tick['symbol'])

    print('Numero de monedas encontradas en el par USDT: #' + str(len(ticks)))

    return ticks

def get_klines(tick):
    klines = client.futures_klines(symbol=tick, interval=Client.KLINE_INTERVAL_1MINUTE, limit=30)
    return klines

def infoticks(tick):
    info = client.futures_ticker(symbol=tick)
    return info

def human_format(volumen):
    magnitude = 0
    while abs(volumen) >= 1000:
        magnitude += 1
        volumen /= 1000.0
    return '%.2f%s' % (volumen, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

def porcentaje_klines(tick, klines, knumber):
    inicial = float(klines[0][4])
    final = float(klines[knumber][4])

    # LONG
    if inicial > final:
        result = round(((inicial - final) / inicial) * 100, 2)
        if result >= variacion:
            info = infoticks(tick)
            volumen = float(info['quoteVolume'])
            if volumen > 100000000 or result >= variacion_100:
                print('LONG: '+tick)
                print('Variacion: ' + str(result) + '%')
                print('Volumen: ' + human_format(volumen))
                print('Precio max: ' + info['highPrice'])
                print('Precio min: ' + info['lowPrice'])
                print('Enviando mensaje a Telegram...')
                enviar_mensaje_html(bot_token, chat_id, 'LONG: '+tick)
                


    # SHORT
    if final > inicial:
        result = round(((final - inicial) / inicial) * 100, 2)
        if result >= variacion:
            info = infoticks(tick)
            volumen = float(info['quoteVolume'])
            if volumen > 100000000 or result >= variacion_100:
                print('SHORT: ' + tick)
                print('Variacion: ' + str(result) + '%')
                print('Volumen: ' + human_format(volumen))
                print('Precio max: ' + info['highPrice'])
                print('Precio min: ' + info['lowPrice'])
                print('')
                print('Enviando mensaje a Telegram...')
                enviar_mensaje_html(bot_token, chat_id, 'SHORT: ' + tick)

    # FAST
    if knumber >= 3:
        inicial = float(klines[knumber-2][4])
        final = float(klines[knumber][4])
        if inicial < final:
            result = round(((final - inicial) / inicial) * 100, 2)
            if result >= variacionfast:
                info = infoticks(tick)
                volumen = float(info['quoteVolume'])
                print('FAST SHORT!: ' + tick)
                print('Variacion: ' + str(result) + '%')
                print('Volumen: ' + human_format(volumen))
                print('Precio max: ' + info['highPrice'])
                print('Precio min: ' + info['lowPrice'])
                print('')
                print('Enviando mensaje a Telegram...')
                enviar_mensaje_html(bot_token, chat_id, 'FAST SHORT!: ' + tick)




while True:
    ticks = buscarticks()
    print('Escaneando monedas...')
    print('')
    for tick in ticks:
        klines = get_klines(tick)
        knumber = len(klines)
        if knumber > 0:
            knumber = knumber - 1
            porcentaje_klines(tick, klines, knumber)
    print('Esperando 30 segundos...')
    print('')
    time.sleep(30)
