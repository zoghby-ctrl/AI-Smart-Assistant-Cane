from machine import Pin, PWM, ADC, time_pulse_us
import time

# --- PIN CONFIGURATION ---
# Define which GPIO pins on the ESP32 are connected to which component
TRIGGER_PIN = 5   # Output: Sends the ultrasonic sound wave
ECHO_PIN = 18     # Input: Receives the bouncing sound wave
BUZZER_PIN = 19   # Output: Active Buzzer for audio warnings
LDR_PIN = 34      # Input (Analog): Measures light levels (0-4095)
LED_PIN = 23      # Output: Safety Flashlight (LED)

# --- HARDWARE SETUP ---
# Initialize the Ultrasonic Sensor Pins
trigger = Pin(TRIGGER_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

# Initialize the Buzzer using PWM (Pulse Width Modulation)
# This allows us to change the tone (frequency) later
buzzer = PWM(Pin(BUZZER_PIN), freq=1000)
buzzer.duty(0) # Start with the buzzer OFF (0% duty cycle)

# Initialize the Light Sensor (LDR)
ldr = ADC(Pin(LDR_PIN))
ldr.atten(ADC.ATTN_11DB) # Set range to read full 0-3.3V voltage

# Initialize the LED Flashlight
light = Pin(LED_PIN, Pin.OUT)
light.value(0) # Ensure light is OFF at startup

# --- GLOBAL VARIABLES ---
LIGHT_LIMIT = 1500       # Threshold for "Darkness" (Adjust if needed)
prev_distance = 0        # Stores the distance from the LAST loop (for speed math)
last_time = time.ticks_ms() # Stores the time of the LAST loop

# --- FUNCTION: MEASURE DISTANCE ---
# Sends a sound pulse and measures how long it takes to return
def get_distance():
    # 1. Send a 10-microsecond High pulse to trigger the sensor
    trigger.value(0)
    time.sleep_us(2)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)
    
    try:
        # 2. Measure how long the Echo pin stays HIGH (in microseconds)
        duration = time_pulse_us(echo, 1, 30000) # Timeout after 30ms
        
        # 3. Calculate Distance: (Time x Speed of Sound) / 2
        # Speed of sound is approx 0.0343 cm/us
        if duration < 0: return 200 # Return 200cm if timeout (no obstacle)
        return (duration * 0.0343) / 2
    except:
        return 200 # Error safety

# --- FUNCTION: SMART BEEP ---
# Changes the sound pattern based on how "Urgent" the danger is
def beep(speed_urgency):
    if speed_urgency > 1.5:
        # CRITICAL DANGER: High pitch, very fast beeping
        buzzer.freq(2000) # High Tone
        buzzer.duty(512)  # Turn Sound ON (50% power)
        time.sleep(0.05)
        buzzer.duty(0)    # Turn Sound OFF
        time.sleep(0.05)
    elif speed_urgency > 0.5:
        # CAUTION: Lower pitch, slower beeping
        buzzer.freq(1000) # Normal Tone
        buzzer.duty(512)
        time.sleep(0.1)
        buzzer.duty(0)
        time.sleep(0.3)
    else:
        # SAFE: Ensure buzzer is silent
        buzzer.duty(0)

print("Ultimate Smart Cane Active")

# --- MAIN SYSTEM LOOP ---
while True:
    # ------------------------------------------------
    # FEATURE 1: AUTOMATIC NIGHT MODE
    # ------------------------------------------------
    light_value = ldr.read() # Read light level (0 = Dark, 4095 = Bright)
    
    if light_value < LIGHT_LIMIT:
        light.value(1) # Too dark? Turn LED ON
    else:
        light.value(0) # Bright enough? Turn LED OFF

    # ------------------------------------------------
    # FEATURE 2: VELOCITY-BASED OBSTACLE DETECTION
    # ------------------------------------------------
    current_time = time.ticks_ms()
    current_dist = get_distance()
    
    # Calculate time difference (dt) in seconds
    dt = time.ticks_diff(current_time, last_time) / 1000.0
    
    # Avoid dividing by zero or super fast loops
    if dt > 0.1:
        # CALCULATE VELOCITY (Speed = Change in Distance / Change in Time)
        # Positive result means approaching the wall.
        speed_cm_s = (prev_distance - current_dist) / dt
        
        risk_score = 0
        
        # --- DECISION TREE (THE "AI" LOGIC) ---
        if current_dist < 30: 
            # Case A: Too close! Panic mode regardless of speed.
            risk_score = 2
        elif current_dist < 100 and speed_cm_s > 20:
            # Case B: Walking FAST towards wall. Warn early!
            risk_score = 1.6
        elif current_dist < 100:
            # Case C: Close, but standing still or walking slow.
            risk_score = 0.6
            
        # Trigger the buzzer if risk is high enough
        if risk_score > 0.5:
            beep(risk_score)
        
        # Save current values for the next loop comparison
        prev_distance = current_dist
        last_time = current_time
        
    time.sleep(0.05) # Small delay to stabilize sensor