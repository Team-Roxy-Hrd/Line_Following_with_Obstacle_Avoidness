from controller import Robot

robot = Robot()
TIME_STEP = 32
MAX_SPEED = 6.28

left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))
left_motor.setVelocity(0)
right_motor.setVelocity(0)

gs = []
for name in ["gs0", "gs1", "gs2"]:
    s = robot.getDevice(name)
    s.enable(TIME_STEP)
    gs.append(s)

ps = []
for i in range(8):
    s = robot.getDevice(f"ps{i}")
    s.enable(TIME_STEP)
    ps.append(s)

OBS = 82

state = "FOLLOW"
avoid_dir = "left"
avoid_timer = 0

stuck_counter = 0
search_phase = 0
wall_counter = 0

# ================= LOOP =================
while robot.step(TIME_STEP) != -1:

    g = [s.getValue() for s in gs]
    p = [s.getValue() for s in ps]

    on_any = max(g) > 5
    front_blocked = p[0] > OBS or p[7] > OBS

    right_val = p[0] + p[1]
    left_val  = p[7] + p[6]

    right_wall = p[0] + p[1] + p[2] > 180
    left_wall  = p[5] + p[6] + p[7] > 180
    near_wall = right_wall or left_wall

    
    tuck_counter = 0

    if near_wall:
        wall_counter += 1
    else:
        wall_counter = 0

    if stuck_counter > 25:
        left_motor.setVelocity(-3)
        right_motor.setVelocity(-3)
        robot.step(50)

        left_motor.setVelocity(-3)
        right_motor.setVelocity(3)
        robot.step(100)

        stuck_counter = 0
        state = "SEARCH"
        continue

    if wall_counter > 40:
        left_motor.setVelocity(-3)
        right_motor.setVelocity(-3)
        robot.step(50)

        left_motor.setVelocity(3)
        right_motor.setVelocity(-3)
        robot.step(100)

        wall_counter = 0
        state = "SEARCH"
        continue

    # ================= FSM =================

    # ===== FOLLOW (FIXED - CENTERED CONTROL) =====
    if state == "FOLLOW":

        if front_blocked:
            avoid_dir = "left" if left_val < right_val else "right"
            avoid_timer = 0
            state = "AVOID"

        elif not on_any:
            state = "SEARCH"

        else:
            # ===== ERROR-BASED LINE FOLLOWING =====

            left_s = g[1]
            right_s = g[2]

            error = right_s - left_s

            base_speed = 3.5

            turn = error * 0.6

            left_speed = base_speed - turn
            right_speed = base_speed + turn

            # clamp
            left_speed = max(-3, min(MAX_SPEED, left_speed))
            right_speed = max(-3, min(MAX_SPEED, right_speed))

            left_motor.setVelocity(left_speed)
            right_motor.setVelocity(right_speed)

    # ===== AVOID =====
    elif state == "AVOID":

        avoid_timer += 1

        if avoid_dir == "left":
            left_motor.setVelocity(-1)
            right_motor.setVelocity(4)
        else:
            left_motor.setVelocity(4)
            right_motor.setVelocity(-1)

        if not front_blocked and avoid_timer > 15:
            state = "RETURN"
            avoid_timer = 0

    # ===== RETURN =====
    elif state == "RETURN":

        avoid_timer += 1

        if on_any:
            state = "FOLLOW"

        elif front_blocked:
            state = "AVOID"
            avoid_timer = 0

        else:
            if avoid_dir == "left":
                left_motor.setVelocity(2.5)
                right_motor.setVelocity(1.5)
            else:
                left_motor.setVelocity(1.5)
                right_motor.setVelocity(2.5)

        if avoid_timer > 80:
            state = "SEARCH"

    # ===== SEARCH =====
    elif state == "SEARCH":

        if on_any:
            state = "FOLLOW"
            search_phase = 0

        elif front_blocked:
            state = "AVOID"
            avoid_timer = 0

        elif right_wall:
            left_motor.setVelocity(2)
            right_motor.setVelocity(4.5)

        elif left_wall:
            left_motor.setVelocity(4.5)
            right_motor.setVelocity(2)

        else:
            search_phase += 1

            if search_phase < 40:
                left_motor.setVelocity(2.8)
                right_motor.setVelocity(2.8)

            elif search_phase < 90:
                left_motor.setVelocity(2.8)
                right_motor.setVelocity(1.8)

            elif search_phase < 140:
                left_motor.setVelocity(1.8)
                right_motor.setVelocity(2.8)

            else:
                search_phase = 0