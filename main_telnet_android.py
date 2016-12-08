import telnetlib
import pynmea2
import time

from key_hit import KBHit

HOST = "localhost"
PORT = 5554
MODE = 0  # 0=simple, 1=todo NMEA


def main():
    tn = telnetlib.Telnet(HOST, PORT)
    print tn.read_until("OK")
    kb = KBHit()
    lat = -22.4265
    lon = -45.4479
    msg = pynmea2.parse("$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D")
    while True:
        if MODE == 0:
            if kb.kbhit():
                c = kb.getarrow()
                if c == 0:
                    lat += 0.0001
                elif c == 2:
                    lat -= 0.0001
                elif c == 1:
                    lon += 0.0001
                else:
                    lon -= 0.0001
            else:
                time.sleep(1)
            send = "geo fix {} {}\n".format(lon, lat)
        else:
            send = str(msg)
        print send,
        tn.write(send)
        tn.read_until("OK")


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception:
            print "Error..."
