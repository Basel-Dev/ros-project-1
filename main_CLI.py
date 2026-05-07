from fleet import Fleet
from drone import Drone
from package import Package
from mission import start_trip
from simulate_B import simulateDrone
import pathFinding
import subprocess

fleet = Fleet()

# تحميل البيانات القديمة
fleet.load_data()

# خريطة
grid = []

def getInputTillValid(passedInput, str=False, num=False):
    x = None
    if str:
        while True:
            x = input(passedInput)
            if not len(x) > 0:
                print("Invalid Input, Please Input a Valid ID")
                continue;
            else:
                break
    elif num:
        while True:
            x = input(passedInput)
            if not len(x) > 0 or not x.isdigit():
                print("Invalid Input, Please Input a valid number.")
                continue;
            else:
                break
    return x

def getIfInRange(coordinate):
    return coordinate > -10 and coordinate < 10
    
def clearTerminal():
    subprocess.run("clear")        

def pressEnterToContinue():
    input("Press Enter to Continue ")

while True:
    clearTerminal()
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

    clearTerminal()
    # =========================================
    # ADD DRONE
    # =========================================
    if choice == "1":

        drone_id = getInputTillValid("Enter Drone ID: ", str=True)
        max_weight = float(
            getInputTillValid("Enter max weight: ", num=True)
        )

        new_drone = Drone(
            drone_id,
            max_weight
        )
        print("Drone Added.")
        fleet.add_drone(new_drone)
        pressEnterToContinue()
        

    # =========================================
    # ADD PACKAGE
    # =========================================
    elif choice == "2":

        package_id = getInputTillValid("Enter Package ID: ", str=True)

        weight = getInputTillValid("Enter Package Weight: ", num=True)
        
        while True:
            print("Range 10x10")
            x = int(getInputTillValid("Destination X: ", num=True))
            y = int(getInputTillValid("Destination Y: ", num=True))
            if not getIfInRange(x) or not getIfInRange(y):
                print("Destination is outside of range, please re-enter destination.")
                continue
            elif (x, y) in pathFinding.getObstacles() :
                print("Destination is in obstacle")
                continue
            else:
                break 

        new_package = Package(
            package_id,
            weight,
            (x, y)
        )

        fleet.add_package(new_package)
        print("Package Added")
        pressEnterToContinue()

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
        pressEnterToContinue()


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
        
        pressEnterToContinue()

    # =========================================
    # RECHARGE ALL DRONES
    # =========================================
    elif choice == "5":
        fleet.recharge_all_drones()
        pressEnterToContinue()

    # =========================================
    # ADD NO-FLY ZONE
    # =========================================
    elif choice == "6":
        obstacle_type = getInputTillValid("Add or Remove? (a/r)", str=True)

        if obstacle_type.lower() == "a":

            x1 = int(getInputTillValid("Start X: ", num=True))
            y1 = int(getInputTillValid("Start Y: ", num=True))
            x2 = int(getInputTillValid("End X: ", num=True))
            y2 = int(getInputTillValid("End Y: ", num=True))

            if getIfInRange(x1) and getIfInRange(x2) and getIfInRange(y1) and getIfInRange(y2):
                pathFinding.add_rectangle_obstacle(x1,x2,y1,y2)
                print("Obstacle added")
            else:
                print("Invalid Obstacles, points are outside range")

        elif obstacle_type == "r":
            pathFinding.clearObstacles()
            print("Obstacles cleared")
        else:
            print("Invalid")
        pressEnterToContinue()

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
                getInputTillValid("Choose drone index: ", str=True)
            )

            print("\n===== PACKAGES =====")

            for i, package in enumerate(fleet.packages):
                print(f"{i}) {package}")

            package_index = int(
                getInputTillValid("Choose package index: ", num=True)
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