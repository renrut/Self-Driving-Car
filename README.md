# Self-Driving-Car
Repo for R/C self driving car. The car is set up with the same configuration as a donkeycar follow [their guide](https://docs.donkeycar.com/guide/build_hardware/) for instructions on building the car.

### Current State
There's not a dependencies install script at the moment. Install dependencies with pip3. To start serving, run `python3 start_script.py` and navigate to `192.168.your.ip:8000` in the webbrowser.

This implementation supports steering the car with W,A,S,D, arrow keys, or a dualshock 4 controller using R2 for throttle, L2 for brake/reverse.
