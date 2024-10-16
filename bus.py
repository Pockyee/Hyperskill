import json
import re
from collections import defaultdict


class BusStop:
    def __init__(self, bus_id, stop_id, stop_name, next_stop, stop_type, a_time):
        self.bus_id = bus_id
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.next_stop = next_stop
        self.stop_type = stop_type
        self.a_time = a_time

    def validate_bus_id(self):
        return isinstance(self.bus_id, int)

    def validate_stop_id(self):
        return isinstance(self.stop_id, int)

    def validate_stop_name(self):
        return bool(
            re.match(r"^[A-Z][\w\s]+(?:Road|Avenue|Boulevard|Street)$", self.stop_name)
        )

    def validate_next_stop(self):
        return isinstance(self.next_stop, int)

    def validate_stop_type(self):
        return bool(re.match(r"^[SOF]?$", self.stop_type))

    def validate_a_time(self):
        return bool(re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", self.a_time))


class Bus:
    def __init__(self, bus_id):
        self.bus_id = bus_id
        self.stops = []
        self.start_stop = None
        self.final_stop = None

    def add_stop(self, stop):
        self.stops.append(stop)

    def start(self, stop):
        self.start_stop = stop

    def final(self, stop):
        self.final_stop = stop


raw_data = json.loads(input())

buses = {}
error_dict = {
    "bus_id": 0,
    "stop_id": 0,
    "stop_name": 0,
    "next_stop": 0,
    "stop_type": 0,
    "a_time": 0,
}

stop_bus_map = defaultdict(set)

for stop in raw_data:
    bus_stop = BusStop(
        bus_id=stop["bus_id"],
        stop_id=stop["stop_id"],
        stop_name=stop["stop_name"],
        next_stop=stop["next_stop"],
        stop_type=stop["stop_type"],
        a_time=stop["a_time"],
    )

    if bus_stop.bus_id not in buses:
        buses[bus_stop.bus_id] = Bus(bus_stop.bus_id)
    buses[bus_stop.bus_id].add_stop(bus_stop)

    stop_bus_map[bus_stop.stop_name].add(bus_stop.bus_id)

    if bus_stop.stop_type == "S":
        buses[bus_stop.bus_id].start(bus_stop)
    if bus_stop.stop_type == "F":
        buses[bus_stop.bus_id].final(bus_stop)

    if not bus_stop.validate_bus_id():
        error_dict["bus_id"] += 1
    if not bus_stop.validate_stop_id():
        error_dict["stop_id"] += 1
    if not bus_stop.validate_stop_name():
        error_dict["stop_name"] += 1
    if not bus_stop.validate_next_stop():
        error_dict["next_stop"] += 1
    if not bus_stop.validate_stop_type():
        error_dict["stop_type"] += 1
    if not bus_stop.validate_a_time():
        error_dict["a_time"] += 1

total_errors = sum(error_dict.values())
print(f"Type and field validation: {total_errors} errors")
for field, count in error_dict.items():
    print(f"{field}: {count}")
text = ""
print("\nLine names and number of stops:")
start_stops = []
final_stops = []
for bus_id, bus in buses.items():
    print(f"Bus ID: {bus_id} stops: {len(bus.stops)}")
    if bus.start_stop and bus.final_stop:
        start_stops.append(bus.start_stop.stop_name)
        final_stops.append(bus.final_stop.stop_name)
    else:
        text = f"There is no start or end stop for the line: {bus_id}"
transfer_stops = [stop for stop, bus_ids in stop_bus_map.items() if len(bus_ids) > 1]
print("\nStart stops:", len(set(start_stops)), sorted(set(start_stops)))
print("Transfer stops:", len(set(transfer_stops)), sorted(transfer_stops))
print("Final stops:", len(set(final_stops)), sorted(set(final_stops)))
print(text)
