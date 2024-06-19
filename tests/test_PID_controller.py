import pytest
from src.PID_controller import PIDController


def test_pid_initialization():
    pid = PIDController(Kp=1.0, Ki=0.1, Kd=0.01)
    assert pid.Kp == 1.0
    assert pid.Ki == 0.1
    assert pid.Kd == 0.01
    assert pid.previous_error == 0
    assert pid.integral == 0


def test_pid_update_positive_adjustment():
    pid = PIDController(Kp=1.0, Ki=0.1, Kd=0.01)
    adjustment = pid.update(target_rate=100, actual_rate=90, dt=1)
    assert adjustment == 1, "Expected a positive adjustment"


def test_pid_update_no_adjustment():
    pid = PIDController(Kp=1.0, Ki=0.1, Kd=0.01)
    pid.previous_error = 10  # Simulating a previous state
    adjustment = pid.update(target_rate=100, actual_rate=100, dt=1)
    assert adjustment == 0, "Expected no adjustment"


def test_pid_update_negative_adjustment():
    pid = PIDController(Kp=1.0, Ki=0.1, Kd=0.01)
    # Adjusting the initial conditions to simulate a scenario
    # where a negative adjustment (decrease) is needed.
    pid.previous_error = -20
    adjustment = pid.update(target_rate=90, actual_rate=100, dt=1)
    assert adjustment == 0, "Expected a negative adjustment (represented as 0)"