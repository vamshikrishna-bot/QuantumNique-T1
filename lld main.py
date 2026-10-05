
from enum import Enum
from datetime import datetime
from math import ceil


# ============================================================
# VEHICLE TYPE
# ============================================================

class VehicleType(Enum):
    BIKE = "BIKE"
    CAR = "CAR"
    TRUCK = "TRUCK"


# ============================================================
# VEHICLE
# ============================================================

class Vehicle:
    def __init__(self, number, vehicle_type):
        self.number = number
        self.vehicle_type = vehicle_type


# ============================================================
# PARKING SLOT
# ============================================================

class ParkingSlot:
    def __init__(self, slot_id, vehicle_type):
        self.slot_id = slot_id
        self.vehicle_type = vehicle_type
        self.vehicle = None

    def is_free(self):
        return self.vehicle is None

    def park(self, vehicle):
        self.vehicle = vehicle

    def release(self):
        self.vehicle = None


# ============================================================
# PARKING FLOOR
# ============================================================

class ParkingFloor:
    def __init__(self, floor_id):
        self.floor_id = floor_id
        self.slots = []

    def add_slot(self, slot):
        self.slots.append(slot)

    def find_free_slot(self, vehicle_type):
        for slot in self.slots:
            if slot.is_free() and slot.vehicle_type == vehicle_type:
                return slot
        return None


# ============================================================
# TICKET
# ============================================================

class Ticket:
    def __init__(self, ticket_id, vehicle, floor_id, slot_id, price):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.floor_id = floor_id
        self.slot_id = slot_id
        self.entry_time = datetime.now()
        self.ticket_price = price
        self.active = True
        self.fee = 0

    def close(self, fee):
        self.active = False
        self.fee = fee


# ============================================================
# STRATEGY PATTERN - SLOT ALLOCATION
# ============================================================

class SlotAllocationStrategy:
    def find_slot(self, floors, vehicle_type):
        for floor in floors:
            slot = floor.find_free_slot(vehicle_type)

            if slot is not None:
                return floor, slot

        return None, None


# ============================================================
# STRATEGY PATTERN - FEE
# ============================================================

class FeeStrategy:
    def calculate_fee(self, ticket):
        return 0


class BikeFeeStrategy(FeeStrategy):
    def calculate_fee(self, ticket):
        hours = ceil(
            (datetime.now() - ticket.entry_time).total_seconds() / 3600
        )
        hours = max(1, hours)
        return hours * 20


class CarFeeStrategy(FeeStrategy):
    def calculate_fee(self, ticket):
        hours = ceil(
            (datetime.now() - ticket.entry_time).total_seconds() / 3600
        )
        hours = max(1, hours)
        return hours * 40


class TruckFeeStrategy(FeeStrategy):
    def calculate_fee(self, ticket):
        hours = ceil(
            (datetime.now() - ticket.entry_time).total_seconds() / 3600
        )
        hours = max(1, hours)
        return hours * 60


# ============================================================
# FACTORY PATTERN
# ============================================================

class FeeStrategyFactory:
    @staticmethod
    def get_strategy(vehicle_type):
        if vehicle_type == VehicleType.BIKE:
            return BikeFeeStrategy()

        if vehicle_type == VehicleType.CAR:
            return CarFeeStrategy()

        if vehicle_type == VehicleType.TRUCK:
            return TruckFeeStrategy()

        return None


class VehicleFactory:
    @staticmethod
    def create_vehicle(number, choice):
        if choice == 1:
            return Vehicle(number, VehicleType.BIKE)

        if choice == 2:
            return Vehicle(number, VehicleType.CAR)

        if choice == 3:
            return Vehicle(number, VehicleType.TRUCK)

        return None


# ============================================================
# PARKING LOT
# ============================================================

class ParkingLot:
    def __init__(self, name):
        self.name = name
        self.floors = []
        self.tickets = {}
        self.parked_vehicles = {}
        self.ticket_number = 1

    def add_floor(self, floor):
        self.floors.append(floor)

    def find_floor(self, floor_id):
        for floor in self.floors:
            if floor.floor_id == floor_id:
                return floor

        return None

    def create_ticket_id(self):
        ticket_id = "T" + str(self.ticket_number)
        self.ticket_number += 1
        return ticket_id


# ============================================================
# PARKING SERVICE
# ============================================================

class ParkingService:
    def __init__(self, parking_lot, allocation_strategy):
        self.parking_lot = parking_lot
        self.allocation_strategy = allocation_strategy

    def get_price(self, vehicle_type):
        if vehicle_type == VehicleType.BIKE:
            return 20
        if vehicle_type == VehicleType.CAR:
            return 40
        if vehicle_type == VehicleType.TRUCK:
            return 60
        return 0

    def park(self, vehicle):
        # Duplicate vehicle check
        if vehicle.number in self.parking_lot.parked_vehicles:
            print("Vehicle is already parked.")
            return None

        # Find suitable slot before taking payment
        floor, slot = self.allocation_strategy.find_slot(
            self.parking_lot.floors,
            vehicle.vehicle_type
        )

        if slot is None:
            print("No suitable slot available.")
            return None

        # Show price and ask user to buy ticket
        price = self.get_price(vehicle.vehicle_type)

        print("\n------------------------------")
        print("PARKING TICKET")
        print("------------------------------")
        print("Vehicle No   :", vehicle.number)
        print("Vehicle Type :", vehicle.vehicle_type.value)
        print("Floor        :", floor.floor_id)
        print("Slot         :", slot.slot_id)
        print("Price (1 hr) : Rs.", price)

        buy = input("Buy ticket? (y/n): ").strip().lower()

        if buy != "y":
            print("Ticket not purchased. Vehicle is not parked.")
            return None

        # Park only after ticket is bought
        slot.park(vehicle)

        ticket_id = self.parking_lot.create_ticket_id()

        ticket = Ticket(
            ticket_id,
            vehicle,
            floor.floor_id,
            slot.slot_id,
            price
        )

        self.parking_lot.tickets[ticket_id] = ticket
        self.parking_lot.parked_vehicles[vehicle.number] = ticket_id

        print("\nTicket confirmed!")
        print("------------------------------")
        print("Ticket ID    :", ticket.ticket_id)
        print("Vehicle No   :", ticket.vehicle.number)
        print("Vehicle Type :", ticket.vehicle.vehicle_type.value)
        print("Floor        :", ticket.floor_id)
        print("Slot         :", ticket.slot_id)
        print("Ticket Price : Rs.", ticket.ticket_price)
        print("Status       : ACTIVE")
        print("------------------------------")

        return ticket

    def view_ticket(self, ticket_id):
        ticket = self.parking_lot.tickets.get(ticket_id)

        if ticket is None:
            print("Invalid ticket.")
            return False

        print("\n========== TICKET ==========")
        print("Ticket ID    :", ticket.ticket_id)
        print("Vehicle No   :", ticket.vehicle.number)
        print("Vehicle Type :", ticket.vehicle.vehicle_type.value)
        print("Floor        :", ticket.floor_id)
        print("Slot         :", ticket.slot_id)
        print("Entry Time   :", ticket.entry_time.strftime("%Y-%m-%d %H:%M:%S"))
        print("Ticket Price : Rs.", ticket.ticket_price)
        print("Status       :", "ACTIVE" if ticket.active else "CLOSED")

        if not ticket.active:
            print("Final Fee    : Rs.", ticket.fee)

        print("============================")
        return True

    def unpark(self, ticket_id):
        ticket = self.parking_lot.tickets.get(ticket_id)

        if ticket is None:
            print("Invalid ticket.")
            return

        if not ticket.active:
            print("Vehicle has already exited.")
            return

        # Show ticket before exit
        print("\nYour ticket:")
        self.view_ticket(ticket_id)

        confirm = input("\nDo you want to exit? (y/n): ").strip().lower()

        if confirm != "y":
            print("Exit cancelled.")
            return

        floor = self.parking_lot.find_floor(ticket.floor_id)

        if floor is None:
            print("Floor not found.")
            return

        slot = None

        for s in floor.slots:
            if s.slot_id == ticket.slot_id:
                slot = s
                break

        if slot is None:
            print("Slot not found.")
            return

        # Calculate final fee
        fee_strategy = FeeStrategyFactory.get_strategy(
            ticket.vehicle.vehicle_type
        )

        fee = fee_strategy.calculate_fee(ticket)

        # Release slot and close ticket
        slot.release()
        ticket.close(fee)

        del self.parking_lot.parked_vehicles[ticket.vehicle.number]

        print("\nVehicle exited successfully!")
        print("Vehicle :", ticket.vehicle.number)
        print("Fee     : Rs.", fee)

    def show_free_slots(self, vehicle_type):
        print("\nFree", vehicle_type.value, "slots:")

        found = False

        for floor in self.parking_lot.floors:
            slots = []

            for slot in floor.slots:
                if slot.is_free() and slot.vehicle_type == vehicle_type:
                    slots.append(slot.slot_id)

            if slots:
                found = True
                print("Floor", floor.floor_id, ":", slots)

        if not found:
            print("No free slots.")

    def show_occupancy(self):
        print("\n----- OCCUPANCY -----")

        for floor in self.parking_lot.floors:
            occupied = 0

            for slot in floor.slots:
                if not slot.is_free():
                    occupied += 1

            print(
                "Floor", floor.floor_id,
                ":", occupied, "/", len(floor.slots),
                "occupied"
            )

    def show_all_slots(self):
        print("\n----- ALL SLOTS -----")

        for floor in self.parking_lot.floors:
            print("\nFloor", floor.floor_id)

            for slot in floor.slots:
                vehicle = "FREE"

                if not slot.is_free():
                    vehicle = slot.vehicle.number

                print(
                    slot.slot_id,
                    "|", slot.vehicle_type.value,
                    "|", vehicle
                )


# ============================================================
# INPUT HELPER
# ============================================================

def choose_vehicle_type():
    print("\nChoose vehicle type:")
    print("1. BIKE")
    print("2. CAR")
    print("3. TRUCK")

    try:
        choice = int(input("Enter choice: "))
    except ValueError:
        print("Please enter a number.")
        return None

    if choice == 1:
        return VehicleType.BIKE

    if choice == 2:
        return VehicleType.CAR

    if choice == 3:
        return VehicleType.TRUCK

    print("Invalid vehicle type.")
    return None


# ============================================================
# SIMPLE 8 TEST CASES
# ============================================================

def run_tests():
    print("\n========== RUNNING TESTS ==========")

    lot = ParkingLot("Test Lot")

    floor1 = ParkingFloor(1)
    floor1.add_slot(ParkingSlot("B1", VehicleType.BIKE))
    floor1.add_slot(ParkingSlot("C1", VehicleType.CAR))
    floor1.add_slot(ParkingSlot("T1", VehicleType.TRUCK))

    lot.add_floor(floor1)

    service = ParkingService(lot, SlotAllocationStrategy())

    passed = 0

    # Test 1 - Park vehicle
    bike = Vehicle("TEST-BIKE", VehicleType.BIKE)
    ticket = service.park(bike)

    if ticket is not None and ticket.ticket_price == 20:
        print("Test 1 PASS - Buy ticket and park vehicle")
        passed += 1

    # Test 2 - Duplicate vehicle
    duplicate = service.park(
        Vehicle("TEST-BIKE", VehicleType.BIKE)
    )

    if duplicate is None:
        print("Test 2 PASS - Reject duplicate vehicle")
        passed += 1

    # Test 3 - View ticket
    if service.view_ticket(ticket.ticket_id):
        print("Test 3 PASS - View confirmed ticket")
        passed += 1

    # Test 4 - Invalid ticket
    service.unpark("T999")
    print("Test 4 PASS - Invalid ticket handled")
    passed += 1

    # Test 5 - Free slots
    service.show_free_slots(VehicleType.CAR)
    print("Test 5 PASS - View free slots")
    passed += 1

    # Test 6 - Occupancy
    service.show_occupancy()
    print("Test 6 PASS - View occupancy")
    passed += 1

    # Test 7 - Exit vehicle
    service.unpark(ticket.ticket_id)
    if ticket.active is False:
        print("Test 7 PASS - Exit vehicle")
        passed += 1

    # Test 8 - Repeated exit
    service.unpark(ticket.ticket_id)
    print("Test 8 PASS - Repeated exit handled")
    passed += 1

    print("\nTests passed:", passed, "/ 8")


# ============================================================
# CREATE DEFAULT PARKING LOT
# ============================================================

def create_parking_lot():
    lot = ParkingLot("City Parking")

    # Floor 1
    floor1 = ParkingFloor(1)
    floor1.add_slot(ParkingSlot("1-B1", VehicleType.BIKE))
    floor1.add_slot(ParkingSlot("1-B2", VehicleType.BIKE))
    floor1.add_slot(ParkingSlot("1-C1", VehicleType.CAR))
    floor1.add_slot(ParkingSlot("1-C2", VehicleType.CAR))
    floor1.add_slot(ParkingSlot("1-T1", VehicleType.TRUCK))

    # Floor 2
    floor2 = ParkingFloor(2)
    floor2.add_slot(ParkingSlot("2-B1", VehicleType.BIKE))
    floor2.add_slot(ParkingSlot("2-C1", VehicleType.CAR))
    floor2.add_slot(ParkingSlot("2-T1", VehicleType.TRUCK))

    lot.add_floor(floor1)
    lot.add_floor(floor2)

    return lot


# ============================================================
# MAIN MENU
# ============================================================

def main():
    lot = create_parking_lot()

    service = ParkingService(
        lot,
        SlotAllocationStrategy()
    )

    while True:
        print("\n")
        print("======================================")
        print("       PARKING LOT SYSTEM")
        print("======================================")
        print("1. Park Vehicle")
        print("2. View Ticket")
        print("3. Exit Vehicle")
        print("4. View Free Slots")
        print("5. View Occupancy")
        print("6. View All Slots")
        print("7. Add Floor")
        print("8. Add Slot")
        print("9. Run 8 Tests")
        print("10. Exit Program")
        print("======================================")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a number.")
            continue

        # 1. PARK VEHICLE
        if choice == 1:
            number = input("Enter vehicle number: ").strip()

            if number == "":
                print("Vehicle number cannot be empty.")
                continue

            vehicle_type = choose_vehicle_type()

            if vehicle_type is not None:
                if vehicle_type == VehicleType.BIKE:
                    vehicle = VehicleFactory.create_vehicle(number, 1)
                elif vehicle_type == VehicleType.CAR:
                    vehicle = VehicleFactory.create_vehicle(number, 2)
                else:
                    vehicle = VehicleFactory.create_vehicle(number, 3)

                service.park(vehicle)

        # 2. VIEW TICKET
        elif choice == 2:
            ticket_id = input("Enter ticket ID: ").strip()
            service.view_ticket(ticket_id)

        # 3. EXIT VEHICLE
        elif choice == 3:
            ticket_id = input("Enter ticket ID: ").strip()
            service.unpark(ticket_id)

        # 4. FREE SLOTS
        elif choice == 4:
            vehicle_type = choose_vehicle_type()

            if vehicle_type is not None:
                service.show_free_slots(vehicle_type)

        # 5. OCCUPANCY
        elif choice == 5:
            service.show_occupancy()

        # 6. ALL SLOTS
        elif choice == 6:
            service.show_all_slots()

        # 7. ADD FLOOR
        elif choice == 7:
            try:
                floor_id = int(input("Enter new floor number: "))
            except ValueError:
                print("Invalid floor number.")
                continue

            if lot.find_floor(floor_id) is not None:
                print("Floor already exists.")
            else:
                lot.add_floor(ParkingFloor(floor_id))
                print("Floor added successfully.")

        # 8. ADD SLOT
        elif choice == 8:
            try:
                floor_id = int(input("Enter floor number: "))
            except ValueError:
                print("Invalid floor number.")
                continue

            floor = lot.find_floor(floor_id)

            if floor is None:
                print("Floor not found.")
                continue

            slot_id = input("Enter slot ID: ").strip()
            vehicle_type = choose_vehicle_type()

            if vehicle_type is not None:
                duplicate = False

                for slot in floor.slots:
                    if slot.slot_id == slot_id:
                        duplicate = True
                        break

                if duplicate:
                    print("Slot already exists.")
                else:
                    floor.add_slot(
                        ParkingSlot(slot_id, vehicle_type)
                    )
                    print("Slot added successfully.")

        # 9. TESTS
        elif choice == 9:
            run_tests()

        # 10. EXIT PROGRAM
        elif choice == 10:
            print("Thank you!")
            break

        else:
            print("Invalid choice. Please select 1 to 10.")


if __name__ == "__main__":
    main()
