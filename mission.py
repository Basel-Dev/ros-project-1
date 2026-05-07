from pathFinding import find_path
from drone import DroneStatus  # هيسترد حالات الدرون
import fleet

# حساب استهلاك البطارية
def battery_use(steps, weight):
    return steps * (1 + weight * 0.1)


# التحقق من البطارية
def can_fly(drone, required_battery):
    return drone.battery >= required_battery


# تشغيل الرحلة
def start_trip(drone, package, grid):  # اعملى رحله باستخدام الدرون و الشحنه و الخريطه

    # هات الطريق من مكان الدرون الحالى الى مكان التسليم

    path = find_path(drone.position, package.destination)

    # لو مفيش طريق
    if not path:
        print("No path found")
        return False  # انهاء الداله

    # عدد الخطوات
    steps = len(path)-1

    # حساب البطارية
    battery_needed = battery_use(steps, package.weight)

    # رايح وجاي
    total_battery = battery_needed * 2

    # لو البطارية مش كفاية
    if not can_fly(drone, total_battery):
        print("Battery not enough or path is blocked.")
        return False

    # الدرون بدأ يتحرك
    drone.set_status(DroneStatus.MOVING)

    # الحركة خطوة خطوة
    for step in path:
        drone.position = step
        #drone.consume_battery(1 + package.weight * 0.1)  # كل خطوه تقلل البطاريه
        drone.consume_battery(battery_use(1, package.weight))
        print(f"Drone moving to {step} | Battery: {drone.battery:.1f}%")

        if drone.battery <= 10:
            print("Low battery! Going home...")
            go_home(drone, grid)
            return False

    # تم التسليم
    drone.set_status(DroneStatus.DELIVERING)
    print("Package delivered")

    # الرجوع
    go_home(drone, grid)
    drone.missions += 1
    
    return path


# الرجوع لنقطة البداية
def go_home(drone, grid):

    home_path = find_path(drone.position, (0, 0))

    # لو مفيش طريق
    if not home_path:
        print("Can't return home")
        return

    for step in home_path:
        drone.position = step
        drone.consume_battery(battery_use(1, 0))  # كل خطوه تقلل البطاريه اثناء الرجوع

        print(f"Returning home: {step} | Battery: {drone.battery:.1f}%")

    # بعد الرجوع
    drone.set_status(DroneStatus.IDLE)

    print("Drone returned home safely")
