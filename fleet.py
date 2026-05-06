import json
from drone import Drone, DroneStatus
from package import Package


class Fleet:
    def __init__(self):
        self.drones = []
        self.packages = []

    def add_drone(self, drone):
        for d in self.drones:
            if d.id == drone.id:
                print("Drone ID already exists")
                return
        self.drones.append(drone)
        print("Drone added successfully")

    def add_package(self, package):
        for p in self.packages:
            if p.package_id == package.package_id:
                print("Package ID already exists")
                return
            
        self.packages.append(package)
        print("Package added successfully")


    def recharge_all_drones(self):
        for drone in self.drones:
            drone.battery = 100
        self.save_data()
        print("All drones recharged successfully")

    def save_data(self, filename="fleet.json"):
        data = {
            "drones": [
                {
                    "id": d.drone_id,
                    "max_weight": d.max_weight,
                    "battery": d.battery,
                    "position": d.position,
                    "status": d.status.value
                }
                for d in self.drones
            ],
            "packages": [
                {
                    "id": p.package_id,
                    "weight": p.weight,
                    "destination": p.destination
                }
                for p in self.packages
            ]
        }

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self, filename="fleet.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)

            for d in data["drones"]:
                drone = Drone(d["id"], d["max_weight"])
                drone.battery = d["battery"]
                drone.position = tuple(d["position"])
                drone.status = DroneStatus(d["status"])
                self.drones.append(drone)

            for p in data["packages"]:
                package = Package(
                    p["id"],
                    p["weight"],
                    tuple(p["destination"])
                )
                self.packages.append(package)
            print(data["packages"])

        except FileNotFoundError:
            print("No saved data found")


                 