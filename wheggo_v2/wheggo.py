
class Wheggo:
    def __init__(self, motors):
        self.throttles = [0.,0.,0.,0.]
        self.motors = motors

        # Motor indices
        self.front_left = 0
        self.front_right = 1
        self.rear_left = 2
        self.rear_right = 3

        self.motors_enabled = False

    def update_motors(self):
        if self.motors_enabled:
            for i in range(len(self.throttles)):
                self.motors[i].throttle = self.throttles[i]
        else:
            for i in range(len(self.throttles)):
                self.motors[i].throttle = 0

    def enable_motors(self):
        print("Enabling motors")
        self.motors_enabled = True
        self.update_motors()

    def disable_motors(self):
        print("Disabling motors")
        self.motors_enabled = False
        self.update_motors()


    def handle_message(self, route, msg_type, value):
        if route == '/w/enable':
            if value > 0:
                self.enable_motors()
            else:
                self.disable_motors()

        elif route == '/w/frontleft':
            self.throttles[0] = value
        elif route == '/w/frontright':
            self.throttles[1] = value
        elif route == '/w/rearleft':
            self.throttles[2] = value
        elif route == '/w/rearright':
            self.throttles[3] = value
        elif route == '/w/leftpad':
            (self.throttles[self.front_left], self.throttles[self.rear_left]) = self.throttles_from_pad(value)
        elif route == '/w/rightpad':
            (self.throttles[self.front_right], self.throttles[self.rear_right]) = self.throttles_from_pad(value)
        
        self.update_motors()

    def throttles_from_pad(self, pad_values):
        # Convert pad xy to throttle for that side
        # Full forward is 100% for both motors. Moving left / right
        # slows the rear / forward motor down to 0
        #
        # Sticks fully to the right move only the front motors
        # Sticks fully to the left move only the rear motors
        front_throttle = rear_throttle = pad_values[0]

        delta = pad_values[1] - 0.5
        if delta < 0:
            scale = self.remap(delta, -0.5, 0, 0, 1)
            front_throttle *= scale
        else:
            scale = self.remap(delta, 0, 0.5, 1, 0)
            rear_throttle *= scale
        return (front_throttle, rear_throttle)

    def remap(self, value, start1, stop1, start2, stop2):
        # Remap value into range, like Processing map
        percent = (value - start1) / (stop1 - start1)
        return start2 + percent * (stop2 - start2)

