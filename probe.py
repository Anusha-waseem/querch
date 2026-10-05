from quarchpy.device import getQuarchDevice

dev = getQuarchDevice("USB:QTL2843-03-023")

for cmd in ["*IDN?",
            "MEAS?",
            "CONFig:OUTput:MODE?",
            "REC:AVE?",
            "MEAS:VOLT?",
            "MEAS:CURR?",
            "MEAS:POW?"]:
    try:
        print(f"--- {cmd}")
        print(dev.sendCommand(cmd))
    except Exception as e:
        print(f"    error: {e}")

dev.closeConnection()
