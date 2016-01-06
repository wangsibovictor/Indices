import websocket
import _thread
import time
import json

def on_message(ws, message):
    if message.find("heartbeat") != -1:
        return;
    message_list=json.loads(message)
    message = message_list['message']
    start_pos = message.find("{")
    end_pos = message.find("}")
    message = message[start_pos:end_pos+1]
    message_list = json.loads(message)
    if "last" in message_list:
        print(message_list['last'].replace(',', ''))


def on_error(ws, error):
    print("we received error")
    print(error)



def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def heart_beat(*args):
        while 1:
            time.sleep(1)
            try:
                ws.send("{\"_event\":\"heartbeat\",\"data\":\"h\"}")
            except IOError as e:
                print("Got io error" % (e))

    try:
        #subscribe for S&P500 Index
        ws.send("{\"_event\":\"subscribe\",\"tzID\":55,\"message\":\"pid-8839:\"}")
        ws.send("{\"_event\":\"subscribe\",\"tzID\":55,\"message\":\"pidExt-8839:\"}")
        ws.send("{\"_event\":\"subscribe\",\"tzID\":55,\"message\":\"isOpenPair-8839:\"}")

        #subscribe for A50 Index
        #ws.send("{\"_event\":\"subscribe\",\"tzID\":55,\"message\":\"pid-28930:\"}")
        #ws.send("{\"_event\":\"subscribe\",\"tzID\":55,\"message\":\"pidExt-28930:\"}")
    except IOError as  e:
        print("Got io error" % (e))
    _thread.start_new_thread(heart_beat, ())

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://stream12.forexpros.com:80/echo/websocket",on_message = on_message,on_error = on_error,on_close = on_close)
    ws.on_open=on_open
    ws.run_forever()
