#!/usr/bin/env python3
from math import lcm
from time import time, process_time


class Event:
    def __init__(self, payload, src: "Module", dest: "Module"):
        self.payload = payload
        self.src = src
        self.dest = dest


class Module:
    event_queue: list[Event] = []

    @staticmethod
    def process_event_queue(event_queue: list[Event]) -> None:
        while len(event_queue) > 0:
            current_event = event_queue.pop(0)
            current_event.dest.process_event(current_event)

    def __init__(self, name: str, outputs: list["Module"]) -> None:
        self.name = name
        self.outputs = outputs
        self.pulses_sent = {"low": 0, "high": 0}

    def __str__(self) -> str:
        return f"{type(self).__name__} '{self.name}':\n\tOutputs: {self.get_outputs()}\n\tPulses sent: {self.pulses_sent}"

    def add_outputs(self, outputs: list["Module"]):
        self.outputs.extend(list(outputs))

    def get_outputs(self) -> list[str]:
        return [output.name for output in self.outputs]

    def get_pulses(self) -> dict[str, int]:
        return self.pulses_sent

    def track_pulse(self, event: Event) -> None:
        self.pulses_sent[event.payload] += 1

    def add_event(self, event: Event) -> None:
        self.event_queue.append(event)
        self.track_pulse(event)

    def process_event(self, event: Event) -> None:
        return None


class Broadcaster(Module):
    def __init__(self, name: str, outputs: list[Module]) -> None:
        super().__init__(name, outputs)
        self.events_stage_queue = []

    # May need to do a global queue
    def process_event(self, event: Event) -> None:
        for output in self.outputs:
            self.add_event(Event(event.payload, self, output))

    def run(self):
        for event in self.events_stage_queue:
            self.process_event(event)


class FlipFlop(Module):
    def __init__(self, name: str, outputs: list[Module]) -> None:
        super().__init__(name, outputs)
        self.state = "off"
        self.state_map = {"on": "high", "off": "low"}

    def process_event(self, event: Event) -> None:
        if event.payload == "low":
            if self.state == "off":
                self.state = "on"
            else:
                self.state = "off"
            for output in self.outputs:
                self.add_event(Event(self.state_map[self.state], self, output))


class Conjunction(Module):
    def __init__(
        self, name: str, outputs: list[Module], inputs: list[Module] = None
    ) -> None:
        if inputs == None:
            inputs = []
        self.inputs = inputs
        self.memory = {input: "low" for input in self.inputs}
        super().__init__(name, outputs)

    def __str__(self):
        return f"{super().__str__()}\n\tInputs: {self.get_inputs()}"

    def add_inputs(self, inputs: list["Module"]):
        self.inputs.extend(list(inputs))
        self.memory.update({input: "low" for input in inputs})

    def get_inputs(self) -> list[str]:
        return [input.name for input in self.inputs]

    def process_event(self, event: Event) -> None:
        self.memory[event.src] = event.payload
        if all([value == "high" for value in self.memory.values()]):
            new_payload = "low"
        else:
            new_payload = "high"
        for output in self.outputs:
            self.add_event(Event(new_payload, self, output))


class Button(Module):
    def __init__(self, broadcaster: Broadcaster, name: str = "button") -> None:
        self.name = name
        self.broadcaster = broadcaster
        self.pulses_sent = 0

    def __str__(self):
        return f"{type(self).__name__} '{self.name}':\n\tPulses sent:{{'low':{self.pulses_sent}, 'high': 0}}"

    def press_button(self) -> None:
        self.broadcaster.event_queue.append(Event("low", self, self.broadcaster))
        self.pulses_sent += 1

    def get_pulses(self) -> int:
        return self.pulses_sent


class Output(Module):
    def __init__(
        self, name: str, outputs: list[Module], inputs: list[Module] = None
    ) -> None:
        if inputs == None:
            inputs = []
        self.inputs = inputs
        super().__init__(name, outputs)

    def add_inputs(self, inputs):
        self.inputs.extend(list(inputs))


class Network:
    def __init__(self, module_input: dict[str, list[str]]) -> None:
        self.modules: list[Module] = []
        # Track indexes because the input dict is un-ordered
        idx: dict[str, int] = {}
        # Initial creation of nodes
        for key in module_input.keys():
            if "%" in key or "&" in key:
                if key[0] == "%":
                    mod_type = FlipFlop
                elif key[0] == "&":
                    mod_type = Conjunction
                name = key[1:]
            else:
                mod_type = Broadcaster
                name = key
            self.modules.append(mod_type(name, []))
            idx[key] = len(self.modules) - 1
        # Go back through and associate outputs and inputs to nodes
        #  Doing it this way to avoid having duplicate entries -> just pointing to the single instances of objects
        need_inputs = {
            module: []
            for module in self.modules
            if type(module) == Conjunction or type(module) == Output
        }
        for key in module_input.keys():
            current_module = self.modules[idx[key]]
            current_outputs = list(
                filter(lambda mod: mod.name in module_input[key], self.modules)
            )
            extra_outputs = [
                mod_name
                for mod_name in module_input[key]
                if mod_name not in [mod.name for mod in self.modules]
            ]
            if len(extra_outputs) > 0:
                for output in extra_outputs:
                    mod = Output(output, [])
                    self.modules.append(mod)
                    current_outputs.append(mod)
                    need_inputs[mod] = []
            current_module.add_outputs(current_outputs)
            for output in current_outputs:
                if type(output) == Conjunction or type(output) == Output:
                    need_inputs[output].append(current_module)
        for key in need_inputs.keys():
            key.add_inputs(need_inputs[key])
        self.broadcaster = [mod for mod in self.modules if type(mod) == Broadcaster][0]
        self.button = Button(self.broadcaster)
        self.event_queue = Module.event_queue

    def __str__(self):
        mods_str = "\n".join([str(mod) for mod in self.modules])
        return f"[\n{str(self.button)}\n{mods_str}\n]"

    def process_event_queue(self, event_queue=None) -> None:
        if event_queue is None:
            event_queue = self.event_queue
        Module.process_event_queue(event_queue)

    def run_cycle(self) -> None:
        self.button.press_button()
        self.broadcaster.run()
        self.process_event_queue()

    def run_cycles(self, num_cycles: int) -> None:
        for i in range(num_cycles):
            self.run_cycle()

    def get_all_pulses(self) -> list[int]:
        all_pulses = {"high": 0, "low": self.button.get_pulses()}
        for mod in self.modules:
            all_pulses["high"] += mod.get_pulses()["high"]
            all_pulses["low"] += mod.get_pulses()["low"]
        return all_pulses["high"] * all_pulses["low"]


def handle_input(input: str) -> dict[str, list[str]]:
    f = open(input, "r")
    config_lines = f.read().split("\n")
    f.close()

    module_config = {}
    for line in config_lines:
        name, out = line.split(" -> ")
        outputs = out.split(", ")
        module_config[name] = outputs
    return module_config


# Part 2
# Idea from: https://www.reddit.com/r/adventofcode/comments/18mmfxb/comment/ke5sgxs/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
def get_rx_activation_cycles(network: Network) -> int:
    # There are 4 distinct chains of FlipFlop modules connecting to end Conjunction modules
    # Because of this, they act like binary counters and you can figure out the state of the binary chain required to have the last bit be a `1`
    # Get all of these chains, convert to int and get LCM of these conditions.
    broadcaster = network.broadcaster
    chain_values = []
    for mod in broadcaster.outputs:
        current_mod = mod
        chain = ""
        # FlipFlops that connect to Conjunction modules need to be `1`. Otherwise, they don't. Set them to 0 to get the lowest possible value
        while current_mod is not None and len(current_mod.outputs) > 0:
            if len(current_mod.outputs) == 2 or Conjunction in [
                type(mod) for mod in current_mod.outputs
            ]:
                chain = "1" + chain
            else:
                chain = "0" + chain
            next_ff = [mod for mod in current_mod.outputs if type(mod) == FlipFlop]
            if len(next_ff) > 0:
                current_mod = next_ff[0]
            else:
                current_mod = None
        chain_values.append(chain)
    cycles = [int(chain, 2) for chain in chain_values]
    return lcm(*cycles)


if __name__ == "__main__":
    start_1 = time()
    start_sys_1 = process_time()
    network_1 = Network(handle_input("puzzle input.txt"))
    network_1.run_cycles(1000)

    recorded_pulses = network_1.get_all_pulses()

    end_1 = time()
    end_sys_1 = process_time()
    wall_time_1 = end_1 - start_1
    sys_time_1 = end_sys_1 - start_sys_1

    print(f"Part 1: {recorded_pulses}")
    print(f"Wall time: {wall_time_1:.2f} seconds")
    print(f"System time: {sys_time_1:.2f} seconds")

    start_2 = time()
    start_sys_2 = process_time()
    network_2 = Network(handle_input("puzzle input.txt"))

    min_cycles = get_rx_activation_cycles(network_2)

    end_2 = time()
    end_sys_2 = process_time()
    wall_time_2 = end_2 - start_2
    sys_time_2 = end_sys_2 - start_sys_2

    print(f"Part 2: {min_cycles}")
    print(f"Wall time: {wall_time_2:.2f} seconds")
    print(f"System time: {sys_time_2:.2f} seconds")
