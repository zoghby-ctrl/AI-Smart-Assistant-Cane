# AI-Smart-Assistant-Cane

## Description
This project is a smart mobility aid for the visually impaired powered by an ESP32 microcontroller. Unlike traditional blind sticks, it utilizes a heuristic algorithm to calculate the user's **velocity** relative to obstacles ($\Delta d / \Delta t$), providing dynamic audio warnings based on collision risk rather than just distance. It also features an automated "Night Mode" that activates a safety light in low-visibility conditions.

## Features
* **Velocity-Based Risk Detection:** Distinguishes between a static user standing near a wall (silence) and a user walking fast towards it (alarm).
* **Automatic Night Mode:** Uses an LDR sensor to detect darkness and automatically turns on a high-brightness LED for traffic visibility.
* **Dynamic Audio Feedback:** Controls an active buzzer to produce different urgency levels (Slow Beep vs. Fast Warning) based on the calculated risk score.
* **Power Efficient:** Optimized for battery operation using 5V portable power banks.

## Technology Stack
* **Hardware:** ESP32 DevKit V1, HC-SR04 Ultrasonic Sensor, LDR Photoresistor, Active Buzzer.
* **Language:** MicroPython (Python).
* **Tools:** Thonny IDE (for flashing/coding), Wokwi (for circuit simulation).

## How to Run
1. **Hardware Setup:** Wire the components to the ESP32 according to the provided `circuit_diagram.png`.
2. **Software Prep:** Install **Thonny IDE** and flash the MicroPython firmware onto your ESP32 board.
3. **Deploy Code:** Open `main.py` in Thonny, connect your ESP32 via USB, and click **Run** (or save it to the device as `main.py` for offline use).
4. **Test:** Move your hand towards the sensor at different speeds to hear the variable alarm rates. Cover the LDR to test the automatic light.

## Future Improvements
* **Haptic Feedback:** Integrating a vibration motor for silent alerts in noisy environments.
* **GPS Tracking:** Adding a GSM/GPS module to send location data to family members in emergencies.
* **Battery Management:** Implementing a BMS (Battery Management System) for safer charging and battery level indication.
