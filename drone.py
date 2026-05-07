from enum import Enum 

class DroneStatus(Enum):
    IDLE = "idle"
    MOVING = "moving"
    DELIVERING = "delivering"
    RETURNING = "returning"


class Drone:
    def __init__(self, drone_id, max_weight):
        self.drone_id = drone_id
        self.max_weight = max_weight
        self.battery = 100
        self.position = (0, 0)
        self.missions = 0
        self.status = DroneStatus.IDLE

    def set_status(self, status):
        if isinstance(status, DroneStatus):
            self.status = status

    def consume_battery(self, amount):
        self.battery = max(0, self.battery - amount)

    def __str__(self):
        return f"{self.drone_id} | {self.max_weight} kg | {self.battery:.1f}%"