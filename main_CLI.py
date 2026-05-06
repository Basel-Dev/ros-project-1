from fleet import Fleet
from drone import Drone
from package import Package
from mission import start_trip
from simulate_B import simulateDrone
import pathFinding


fleet = Fleet()

# تحميل البيانات القديمة
fleet.load_data()

# خريطة
grid = []


while True:

    print("\n===== DRONE DELIVERY SYSTEM =====")

    print("1) Add Drone")
    print("2) Add Package")
    print("3) Show Drones")
    print("4) Show Packages")
    print("5) Recharge All Drones")
    print("6) Add No-Fly Zone")
    print("7) Start Simulation")
    print("0) Save and Exit")

    choice = input("\nChoose an option: ")

    # =========================================
    # ADD DRONE
    # =========================================
    if choice == "1":

        drone_id = input("Enter drone ID: ")
        max_weight = float(
            input("Enter max weight: ")
        )

        new_drone = Drone(
            drone_id,
            max_weight
        )

        fleet.add_drone(new_drone)

    # =========================================
    # ADD PACKAGE
    # =========================================
    elif choice == "2":

        package_id = input("Enter package ID: ")

        weight = float(
            input("Enter package weight: ")
        )

        x = int(input("Destination X: "))
        y = int(input("Destination Y: "))

        new_package = Package(
            package_id,
            weight,
            (x, y)
        )

        fleet.add_package(new_package)

    # =========================================
    # SHOW DRONES
    # =========================================
    elif choice == "3":

        if not fleet.drones:
            print("No drones available")

        else:
            print("\n===== DRONES =====")

            for drone in fleet.drones:
                print(drone)

    # =========================================
    # SHOW PACKAGES
    # =========================================
    elif choice == "4":

        if not fleet.packages:
            print("No packages available")

        else:
            print("\n===== PACKAGES =====")

            for package in fleet.packages:
                print(package)

    # =========================================
    # RECHARGE ALL DRONES
    # =========================================
    elif choice == "5":

        fleet.recharge_all_drones()

    # =========================================
    # ADD NO-FLY ZONE
    # =========================================
    elif choice == "6":

        obstacle_type = input(
            "Horizontal or Vertical? (h/v): "
        )

        if obstacle_type == "h":

            x1 = int(input("Start X: "))
            x2 = int(input("End X: "))
            y = int(input("Y position: "))

            pathFinding.add_horizontal_obstacle(
                x1,
                x2,
                y
            )

            print("Horizontal obstacle added")

        elif obstacle_type == "v":

            x = int(input("X position: "))
            y1 = int(input("Start Y: "))
            y2 = int(input("End Y: "))

            pathFinding.add_vertical_obstacle(
                x,
                y1,
                y2
            )

            print("Vertical obstacle added")

        else:
            print("Invalid obstacle type")

    # =========================================
    # START SIMULATION
    # =========================================
    elif choice == "7":

        if not fleet.drones:
            print("No drones available")

        elif not fleet.packages:
            print("No packages available")

        else:

            print("\n===== DRONES =====")

            for i, drone in enumerate(fleet.drones):
                print(f"{i}) {drone}")

            drone_index = int(
                input("Choose drone index: ")
            )

            print("\n===== PACKAGES =====")

            for i, package in enumerate(fleet.packages):
                print(f"{i}) {package}")

            package_index = int(
                input("Choose package index: ")
            )

            drone = fleet.drones[drone_index]
            package = fleet.packages[package_index]

            path = start_trip(
                drone,
                package,
                grid
            )

            if path:

                simulateDrone(
                    drone,
                    package,
                    path
                )

    # =========================================
    # EXIT
    # =========================================
    elif choice == "0":

        fleet.save_data()

        print("Data saved successfully")
        print("Exiting program...")

        break

    # =========================================
    # INVALID CHOICE
    # =========================================
    else:

        print("Invalid choice")