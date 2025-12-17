import cv2
import mediapipe as mp
import serial
import time
import sys

# ---------- USER SETTINGS ----------
SERIAL_PORT = "COM8"   # <- CHANGE to your Arduino port, e.g. "COM3" (Windows) or "/dev/ttyACM0" on Linux
BAUDRATE = 9600
CAMERA_ID = 0          # default webcam
DEBOUNCE_TIME = 0.5    # seconds to hold a gesture before sending repeated identical commands
# ---------- END SETTINGS ----------

# Serial init
try:
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    time.sleep(2)  # wait for Arduino reset
except Exception as e:
    print(f"Error opening serial port {SERIAL_PORT}: {e}")
    sys.exit(1)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(CAMERA_ID)
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.6, min_tracking_confidence=0.5)

last_command = None
last_sent_time = 0

def fingers_up(hand_landmarks):
    """
    Return number of fingers up (0-5) using landmark logic.
    Works for a single detected hand (assumed to be roughly upright).
    """
    # landmark indexes for tips: thumb(4), index(8), middle(12), ring(16), pinky(20)
    tips = [4, 8, 12, 16, 20]
    count = 0
    lm = hand_landmarks.landmark

    # For fingers except thumb: compare tip y to pip y (tip lower on image => finger up)
    # Note: image coords y increase downward, so tip.y < pip.y => finger up
    if lm[tips[1]].y < lm[tips[1]-2].y:  # index
        count += 1
    if lm[tips[2]].y < lm[tips[2]-2].y:  # middle
        count += 1
    if lm[tips[3]].y < lm[tips[3]-2].y:  # ring
        count += 1
    if lm[tips[4]].y < lm[tips[4]-2].y:  # pinky
        count += 1

    # Thumb: compare tip.x to ip.x depending on handness
    # Simple heuristic: thumb is up if tip.x is to the right of ip.x for right hand, left for left hand
    # We'll use x difference magnitude:
    if abs(lm[tips[0]].x - lm[tips[0]-2].x) > 0.03:
        # check direction relative to wrist (landmark 0)
        if lm[tips[0]].x > lm[0].x:  # thumb to right of wrist
            # likely right hand — thumb extended outward
            if lm[tips[0]].x > lm[tips[0]-2].x:
                count += 1
        else:
            # likely left hand
            if lm[tips[0]].x < lm[tips[0]-2].x:
                count += 1

    return count

def map_count_to_command(count):
    """Map finger count to serial command char"""
    if count == 0:
        return 'S'  # stop
    elif count == 1:
        return 'F'  # forward
    elif count == 2:
        return 'B'  # backward
    elif count == 3:
        return 'L'  # left
    elif count == 4:
        return 'R'  # right
    elif count == 5:
        return 'S'  # five fingers => also stop (or you can choose other behavior)
    else:
        return 'S'

print("Starting. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("No camera frame.")
        break

    # Flip for natural mirror-like display
    frame = cv2.flip(frame, 1)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(img_rgb)

    display_text = "No hand"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            count = fingers_up(hand_landmarks)
            cmd = map_count_to_command(count)
            display_text = f"Fingers: {count} -> {cmd}"

            # Debounce: only send if command changed or if enough time has passed
            now = time.time()
            if cmd != last_command or (now - last_sent_time) > DEBOUNCE_TIME:
                try:
                    ser.write(cmd.encode('utf-8'))
                    # Optionally print debug
                    print(f"Sent {cmd} (fingers={count})")
                    last_command = cmd
                    last_sent_time = now
                except Exception as e:
                    print("Serial write error:", e)

            # Only one hand expected, break after processing first
            break

    # draw UI text
    cv2.putText(frame, display_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    cv2.imshow("Gesture Control - Press q to quit", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# cleanup
cap.release()
hands.close()
ser.close()
cv2.destroyAllWindows()
print("Stopped.")
