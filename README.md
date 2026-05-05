# 🤖 Robust Line Following Robot with Obstacle Avoidance

A Webots-based autonomous robot that performs **robust line following**, **obstacle avoidance**, and **intelligent recovery behaviors** using a Finite State Machine (FSM).

---

## 📌 Features

* ✅ Smooth line following using a proportional controller (P-control)
* ✅ Real-time obstacle detection using distance sensors
* ✅ Dynamic obstacle avoidance (left/right decision)
* ✅ Automatic return to the line after avoidance
* ✅ Intelligent search behavior when the line is lost
* ✅ Recovery mechanisms for stuck and wall conditions

---

## 🧠 System Architecture

The robot is controlled using a **Finite State Machine (FSM)** with the following states:

* **FOLLOW** → Track the line smoothly
* **AVOID** → Avoid obstacles
* **RETURN** → Return back to the line
* **SEARCH** → Find the line when lost

---

## 🎮 Simulation Environment

* Platform: **Webots**
* Robot: **E-puck**
* Arena:

  * Textured floor with a closed-loop black line
  * Multiple obstacles (boxes) placed both on and off the line

---

## 🔌 Sensors Used

### Line Sensors

* `gs0`, `gs1`, `gs2`
* Detect line presence and position

### Distance Sensors

* `ps0` → `ps7`
* Used for obstacle detection and wall proximity

---

## ⚙️ Control Strategy

### Line Following (P-Control)

The robot adjusts its direction based on the error between left and right sensors:

```python
error = right_sensor - left_sensor
turn = Kp * error
```

* Ensures smooth and stable movement
* Reduces oscillations

---

## 🚧 Obstacle Avoidance

* Detects obstacles using front sensors (`ps0`, `ps7`)
* Chooses avoidance direction dynamically:

  * Turns toward the side with more space
* Uses timed maneuvering to bypass obstacles

---

## 🔁 Return to Line

* After avoidance, the robot enters **RETURN state**
* Moves in a curved path depending on avoidance direction
* Immediately switches to FOLLOW when the line is detected

---

## 🔍 Search Behavior (Line Lost)

When the robot loses the line:

* Performs a **progressive search pattern**
* Expands movement radius over time (spiral-like behavior)
* Avoids walls while searching

---

## 🛟 Recovery Mechanisms

### Stuck Recovery

* If robot doesn't progress:

  * Moves backward
  * Rotates to escape

### Wall Avoidance Recovery

* Detects prolonged proximity to walls
* Executes escape maneuver

---

## 🧪 Test Scenarios

✔ Obstacle placed directly on the line
✔ Obstacle placed off the line
✔ Line loss and recovery
✔ Narrow spaces and wall interaction

---

## 📊 Performance

* ✔ Smooth tracking with minimal oscillation
* ✔ Reliable obstacle avoidance
* ✔ Fast recovery to line after deviation
* ✔ Stable behavior in complex environments

---

## 🗂 Project Structure

```
📁 project/
 ├── controller.py
 ├── world.wbt
 ├── line.png
 └── README.md
```

---

## 🚀 How to Run

1. Open **Webots**
2. Load the provided `.wbt` world file
3. Attach the controller to the E-puck robot
4. Click **Run**

---

## 🧑‍💻 Author

* Hossam Hassan

---

## 📌 Notes

* Designed for academic evaluation (Robotics / AI course)
* Easily extendable with:

  * PID control
  * Mapping
  * Path planning algorithms

---

## ⭐ Future Improvements

* Full PID controller for better accuracy
* Machine learning-based line detection
* Dynamic path planning (A*, GA)

---

## 🏁 Final Result

A **robust autonomous robot** capable of handling:

* Dynamic obstacles
* Line tracking
* Recovery scenarios

All in a fully simulated environment 🎯

---
