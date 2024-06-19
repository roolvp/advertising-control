class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.previous_error = 0
        self.integral = 0

    def update(self, target_rate, actual_rate, dt):
        """
        Update the PID controller.
        
        :param target_rate: The desired rate of spend.
        :param actual_rate: The current rate of spend.
        :param dt: Time interval.
        :return: Adjustment to be made.
        """
        error = target_rate - actual_rate
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt
        control_variable = (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)
        self.previous_error = error
        return int(control_variable > 0)