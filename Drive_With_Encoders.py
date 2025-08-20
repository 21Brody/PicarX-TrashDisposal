from picarx import Picarx
import time


# Create PiCar-X instance
px = Picarx()


# --- CONFIGURATION ---
DISTANCE_METERS = 10                # Target distance in meters
WHEEL_DIAMETER = 0.066              # Wheel diameter in meters
WHEEL_CIRCUMFERENCE = 3.1416 * WHEEL_DIAMETER
ENCODER_TICKS_PER_REV = 40
TARGET_TICKS = int(DISTANCE_METERS / WHEEL_CIRCUMFERENCE * ENCODER_TICKS_PER_REV)
SPEED = 30  # motor speed (0-100)


def reset_encoders():
    """Reset wheel encoder counts to zero."""
    px.set_motor_power(0, 0)
    px.reset_encoders()


def drive_forward_distance():
    """Drives the PiCar-X forward for a given distance in meters."""
    reset_encoders()
    px.forward(SPEED)
    print(f"Target ticks: {TARGET_TICKS}")


    while True:
        # Get encoder readings
        left_ticks, right_ticks = px.get_motor_encoder()
        avg_ticks = (abs(left_ticks) + abs(right_ticks)) // 2


        # Debug print
        print(f"Ticks: L={left_ticks}, R={right_ticks}, Avg={avg_ticks}")


        # Stop when we’ve reached the target distance
        if avg_ticks >= TARGET_TICKS:
            break


        time.sleep(0.05)


    # Stop motors after reaching target distance
    px.stop()
    print("Reached target distance!")


if __name__ == "__main__":
    try:
        drive_forward_distance()
    except KeyboardInterrupt:
        px.stop()
        print("Stopped manually.")
