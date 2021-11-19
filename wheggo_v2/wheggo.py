
class Wheggo:
    def __init__(self, motors):
        self.throttles = [0.,0.,0.,0.]
        self.motors = motors
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
        if route == '/1/enable':
            if value > 0:
                self.enable_motors()
            else:
                self.disable_motors()

        if route == '/1/frontleft':
            self.throttles[0] = value
        if route == '/1/frontright':
            self.throttles[1] = value
        if route == '/1/rearleft':
            self.throttles[2] = value
        if route == '/1/rearright':
            self.throttles[3] = value

        self.update_motors()