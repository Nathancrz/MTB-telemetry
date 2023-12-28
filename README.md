# MTB telemetry

This is an homemade project of on bike data acquisition and exploitation to enhance bike's performance (yet to be updated)

![alt text](https://github.com/Nathancrz/MTB-telemetry/blob/main/pictures/bike%20profile.png)

## Material :
![alt text](https://github.com/Nathancrz/MTB-telemetry/blob/main/pictures/systeme%20complet.jpeg)
 - Raspberry pi 4B 1 Gb w/ 64 Gb sd card to run the OS and scripts
 - 8 Gb flash drive (auto mounted) to record on
 - 2 linear potentiometers (here 150mm and 100mm)
 - ADC to read the pots value (here an ADS1115)
 - Accelerometer (MPU6050)
 - Screen (SSD1306)
 - Button, breadbord (cut to the minimum width needed), jump wires
 - 18650 batteries and battery module for itinerant power
 - Power bank to help with autonomy
 - Three pins connectors (to have plug and play sensors)
 - Custom fitted hard and insulated case
 - On bike mounts for the brain and for the pots

## Code :
![alt text](https://github.com/Nathancrz/MTB-telemetry/blob/main/testruns/26december/polts26dec/run%207.svg)

Both the data logger and the data analysis programs are written in Python (see the [Code folder](https://github.com/Nathancrz/MTB-telemetry/tree/main/Code))
The analysis outputs the 9 following graphics :
 - travel during the run (both front and rear)
 - travel histogram
 - travel cloud of dots
 - bike balance during the run
 - suspensions' speed histogram
 - suspensions' speed cloud of dots
 - main triangle's acceleration during the run
 - bike balance histogram
 - general statistics

## Noticeable results 
![alt text](https://github.com/Nathancrz/MTB-telemetry/blob/main/testruns/Evolution%20du%20temps.svg)

During the first batch of tests, the time significatively dropped to only 2s of my personnal best (although i was out of shape), but the result was hard to interpret.
During the second batch, the time dropped rapidely with an unconfortable bike handling, which was later corrected to hit a new performance ceiling 11% below the previous one 
