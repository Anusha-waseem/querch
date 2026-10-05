#!/bin/bash

# go to the folder where this script is
cd "$(dirname "$0")"

# 1. compile the java files
javac ListEnergy.java Analyze.java

# 2. close old QIS (if any) and reset the quarch device so it starts clean
python3 -c "from quarchpy.qis import closeQis; closeQis()" > /dev/null 2>&1
python3 -c "from quarchpy.device import getQuarchDevice; getQuarchDevice('USB:QTL2843-03-023').sendCommand('*RST')" > /dev/null 2>&1
sleep 10

# 3. start QIS (Quarch server)
python3 -c "from quarchpy.qis import startLocalQis; startLocalQis()"
sleep 10

# 4. run the experiment (saves raw data in results_list_java)
java ListEnergy

# 5. calculate average energy
java Analyze

# 6. close QIS
python3 -c "from quarchpy.qis import closeQis; closeQis()"
