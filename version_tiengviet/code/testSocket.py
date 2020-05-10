import websocket
import socket
REMOTE_SERVER = "www.google.com"
def is_connected():
  try:
    host = socket.gethostbyname(REMOTE_SERVER)
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False
while(True):
    if(is_connected()):
        print("Connect...")
        try:
            import thread
        except ImportError:
            import _thread as thread
        import time


        def on_message(ws, message):
            print(message)


        def on_error(ws, error):
            print(error)


        def on_close(ws):
            print("### closed ###")


        trigger_up = "tiến lên"
        trigger_up1 = "tiến"

        trigger_down = "lùi lại"
        trigger_down1 = "lùi"

        trigger_left = "sang trái"
        trigger_left1 = "trái"
        trigger_left2 = "rẽ trái"

        trigger_right = "sang phải"
        trigger_right1 = "rẽ phải"
        trigger_right2 = "phải"

        trigger_stop1 = "dừng"
        trigger_stop = "dừng lại"
        key = "Ok Google"


        def on_open(ws):
            def run(*args):
                while 1:
                    list = listen()
                    ws.send(list)
                    if list == trigger_up or list == trigger_up1:
                        ws.send("Len")
                        print("Len")
                    elif list == trigger_down or list == trigger_down1:
                        ws.send("Xuong")
                        print("Xuong")
                    elif list == trigger_left or list == trigger_left1 or list == trigger_left2:
                        ws.send("Trai")
                        print("Trai")
                    elif list == trigger_right or list == trigger_right1 or list == trigger_right2:
                        ws.send("Phai")
                        print("Phai")
                    elif list == trigger_stop or list == trigger_stop1:
                        ws.send("Dung")
                        print("Dung")
                    time.sleep(1)
                ws.close()
                print("thread terminating...")

            thread.start_new_thread(run, ())


        import speech_recognition
        import time

        recognizer = speech_recognition.Recognizer()

        print("Beginning to listen...")


        def listen():
            start = time.time()
            with speech_recognition.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, phrase_time_limit=2)
            try:
                # print(recognizer.recognize_google(audio,language='vi-VN'))
                text = recognizer.recognize_google(audio, language='vi-VN')
                # print("true")
                print((time.time() - start))
                # print(text)
                return text
            except speech_recognition.UnknownValueError:
                print("Could not understand audio")
            print(time.time() - start)
            return ""

        if __name__ == "__main__":
            websocket.enableTrace(True)
            ws = websocket.WebSocketApp("ws://192.168.137.1:8080",
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)
            ws.on_open = on_open
            ws.run_forever()

    else:
        print("Can't Connect")
