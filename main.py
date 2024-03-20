from ipx800.ipx800 import *
import paho.mqtt.client as mqtt
import sdnotify
import time

ipx = IPX800("http://192.168.1.200", "m@keydAPI")

MqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,"IPX800")
MqttClient.connect("192.168.1.40",1883)
MqttClient.loop_start()

n = sdnotify.SystemdNotifier()

delay = 5

while(True):
    time.sleep(delay)
    n.notify("READY=1")
    try:
        kw_ECS = ipx.counters[0].value
        kw_Chauffage = ipx.counters[1].value
        salon_temp = ipx.THLextensions[0].temperature
        salon_humidity = ipx.THLextensions[0].humidity
        salon_luminosity = ipx.THLextensions[0].luminosity
        ext_temp = ipx.THLextensions[1].temperature
        ext_humidity = ipx.THLextensions[1].humidity
        ext_luminosity = ipx.THLextensions[1].luminosity
    except Exception:
        print("communication error")
        pass
        continue
    print(f"kw_ECS : {kw_ECS}")
    print(f"kw_Chauffage : {kw_ECS}")
    print(f"salon_temp : {salon_temp}")
    print(f"salon_humidity : {salon_humidity}")
    print(f"salon_luminosity : {salon_luminosity}")
    print(f"exterieur_temp : {ext_temp}")
    print(f"exterieur_humidity : {ext_humidity}")
    print(f"exterieur_luminosity : {ext_luminosity}")

    result = MqttClient.publish("IPX800/kw_ECS", kw_ECS)
    status = result[0]
    if status == 0:
        print(f"Send msg")
    else:
        print(f"Failed to send message to topic")

    MqttClient.publish("IPX800/kw_Chauffage", kw_Chauffage)
    MqttClient.publish("IPX800/salon_temp",salon_temp)
    MqttClient.publish("IPX800/salon_humidity", salon_humidity)
    MqttClient.publish("IPX800/salon_luminosity", salon_luminosity)
    MqttClient.publish("IPX800/exterieur_temp", ext_temp)
    MqttClient.publish("IPX800/exterieur_humidity", ext_humidity)
    MqttClient.publish("IPX800/exterieur_luminosity", ext_luminosity)
    