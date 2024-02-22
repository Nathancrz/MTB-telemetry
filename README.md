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

Total price as shown : approx 275€

## Code :
![code's output for the run 7](https://github.com/Nathancrz/MTB-telemetry/blob/main/testruns/26december/polts26dec/run%207%20v2.png)

Both the data logger and the data analysis programs are written in Python (see the [Code folder](https://github.com/Nathancrz/MTB-telemetry/tree/main/Code))
The analysis outputs the 9 following graphics :
 - [Travel during the run (both front and rear)](https://github.com/Nathancrz/MTB-telemetry/wiki/Travel-during-the-run-(both-front-and-rear))
 - [Travel histogram](https://github.com/Nathancrz/MTB-telemetry/wiki/Travel-histogram)
 - [Travel cloud of dots](https://github.com/Nathancrz/MTB-telemetry/wiki/Travel-cloud-of-dots)
 - [Bike balance during the run](https://github.com/Nathancrz/MTB-telemetry/wiki/bike-balance-during-the-run)
 - [Suspensions speed histogram](https://github.com/Nathancrz/MTB-telemetry/wiki/Suspensions-speed-histogram)
 - [Suspensions speed cloud of dots](https://github.com/Nathancrz/MTB-telemetry/wiki/Suspensions-speed-cloud-of-dots)
 - [Main triangle's acceleration during the run](https://github.com/Nathancrz/MTB-telemetry/wiki/Main-triangle's-acceleration-during-the-run)
 - [Bike balance histogram](https://github.com/Nathancrz/MTB-telemetry/wiki/Bike-balance-histogram)
 - [General statistics](https://github.com/Nathancrz/MTB-telemetry/wiki/General-statistics-graph)

## Noticeable results :

### Time drop :
![alt text](https://github.com/Nathancrz/MTB-telemetry/blob/main/testruns/Evolution%20du%20temps.svg)

During the first batch of tests, the time significatively dropped to only 2s of my personnal best (although i was out of shape), but the result was hard to interpret.
During the second batch, the time dropped rapidely with an unconfortable bike handling, which was later corrected to hit a new performance ceiling 11% below the previous one with a very smooth ride.

![alt text](https://github.com/Nathancrz/MTB-telemetry/blob/main/testruns/comparaison%20tuyau%20record.png)

Even more interesting, this graph shows that the gap have been dug very evenly through the run so the advantage given should be scalable to every segment.

### The Problem of acceleration :
![alt text](https://github.com/Nathancrz/MTB-telemetry/blob/main/testruns/Acce%CC%81le%CC%81ration%203%20axes%20runs%201%2C%203%2C%207.png)

As the confort increases, we could have expected the average acceleration to drop. But at first sight, it seems that nothing really changed.

![alt text](https://github.com/Nathancrz/MTB-telemetry/blob/main/testruns/Acc%20moy.svg)

But conter intuitively, the average increased very significantly. One interpretation could be that confort helps taking higer accelerations with more ease and get back to speed faster after braking.

![alt text](https://github.com/Nathancrz/MTB-telemetry/blob/main/testruns/comparaison%20accelerations%201%2C%203%2C%207%20(non%20cut).jpg)

So with this idea in mind, we could compare the frame's acceleration to the GPS acceleration to phase out the "speed" from the recording and only get the vibrations but the latest runs still top the measures.

![alt text](https://github.com/Nathancrz/MTB-telemetry/blob/main/testruns/fft%20moyenne%CC%81e%200%2C%203%2C%207.png)

Finally, we can do a Fast Fourrier Transform (FFT) to show some in-depth evolution but, apart from a small change close to 15Hz, the smoothest the ride is, the higher the norm of each frequency of the FFT gets.

Therefore, confort should not be looked through the vibrations of the frame. Two possible evolutions could be to rely on an actual speed sensor to measure the bike's speed, and to record the vivration going through the body of the rider, to see if the confort can be accurately measured.
