from quarchpy.device import scanDevices
from quarchpy.qis import isQisRunning, startLocalQis

if not isQisRunning():
    print("starting QIS...")
    startLocalQis()

print(scanDevices('QIS'))

