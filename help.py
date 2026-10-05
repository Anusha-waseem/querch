from quarchpy.device import getQuarchDevice

dev = getQuarchDevice("USB:QTL2843-03-023")

for topic in ["HELP MEASURE", "HELP RECORD", "HELP CONFIG", "HELP AVERAGING"]:
    print("=" * 60)
    print(topic)
    print("=" * 60)
    print(dev.sendCommand(topic))

dev.closeConnection()

