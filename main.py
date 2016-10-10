#!/usr/local/bin/python3
import sys
import time
import os
import binascii

if len(sys.argv) == 1 or '-i' in sys.argv:
    raw_instructions = sys.stdin.readline().strip()
else:
    raw_instructions = open(sys.argv[1], mode="r").read()

if '-d' in sys.argv:
    debug = True
else:
    debug = False


def format_instructions(raw):
    """Split into chunks of four and turn into integer"""
    result = []
    while raw:
        result.append(int(raw[:4], 2))
        raw = raw[4:]
    return result


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


"0010000001010100"


class WentelVirtualMachine(object):
    def _concact_address(self, a: int, b: int) -> int:
        """Concatenates two binary numbers into another binary number"""
        return int("{:b}{:b}".format(a, b), 2)

    def load_instructions(self, instructions):
        # warning not thread safe
        for instruction, i in zip(reversed(instructions), range(len(instructions))):
            self.memory[i] = instruction
        self.memory.reverse()
        for i, mem in enumerate(self.memory):
            if mem != 0b0000:
                self.execution_pointer = i
                break

    def increment(self):
        self.memory[self.memory_pointer] += 1

    def decrement(self):
        self.memory[self.memory_pointer] -= 1

    def left(self):
        self.memory_pointer -= 1

    def right(self):
        self.memory_pointer += 1

    def ifexec(self):
        if self.memory[
            # concatenate the memory addresses held by...
            self._concact_address(self.memory[self.memory_pointer + 1],  # the memory value of the next memory address
                                  self.memory[self.memory_pointer + 2])  # (and the one after that)
            # to get the address we are going to check out in the memory -> outer layer

        ] == self.memory[self.memory_pointer]:  # to the value of the current memory address
            self.execution_pointer = self._concact_address(
                self.memory[self.memory_pointer + 3],
                self.memory[self.memory_pointer + 4]
            )  # that sets the execution pointer to the address after the next address
            # now we need to move the execution pointer four places forward;
            # twice for each memory address
            self.execution_pointer += 4

    def jump(self):
        # set the current memory pointer...
        self.memory_pointer = \
            self._concact_address(
                self.memory[self.execution_pointer + 1],
                # to the memory value of the memory address after the current one
                self.memory[self.execution_pointer + 2],  # and after that one
            )
        # move execution pointer two places forward, once
        # for every memory address
        self.execution_pointer += 2

    def deposit(self):
        self.memory[self.memory_pointer] = self.execution_pointer

    def noop(self):
        pass

    def debug_state(self):
        clear_screen()
        print(' '.join([format(item, '04b') for item in
                        self.memory])[
              :150] + '\n' + ' ' * self.execution_pointer * 5 + '^' + '\n' + ' ' * 5 * self.memory_pointer + '^')

    def __init__(self):
        self.memory = [0b0000] * 2 ** 4
        self.memory_pointer = 0b00000000
        self.execution_pointer = 0b00000000
        self.opcodes = {
            0b0000: self.noop,
            0b0001: self.ifexec,
            0b0010: self.jump,
            0b0011: self.deposit,
            0b0100: self.increment,
            0b0101: self.decrement,
            0b0110: self.left,
            0b0111: self.right
        }

    def start(self, instructions, debug=False):
        self.load_instructions(instructions)
        while self.execution_pointer != 0b11111111:
            if debug:
                self.debug_state()
                time.sleep(1)
            try:
                self.opcodes[self.memory[self.execution_pointer]]()
            except KeyError as e:
                sys.stderr.write("Fatal Error: Invalid Opcode")
                sys.exit(1)
            except IndexError as e:
                # no more instructions, quit
                sys.exit(0)
            self.execution_pointer += 1


class WentelVirtualMachineWithOutput(WentelVirtualMachine):
    _buffer = ''

    def _render_output(self):
        sys.stdout.write(binascii.unhexlify('%x' % int(self._buffer, 2)).decode('ascii'))
        sys.stdout.flush()
        self._buffer = ''

    def _check_buffer(self):
        """If the buffer is ready to be rendered, render it."""
        if len(self._buffer) == 8:
            self._render_output()

    def zero(self):
        self._buffer += '0'
        self._check_buffer()

    def one(self):
        self._buffer += '1'
        self._check_buffer()

    def __init__(self):
        super().__init__()
        self.opcodes.update({
            0b1000: self.zero,
            0b1001: self.one,
        })


vm = WentelVirtualMachineWithOutput()
vm.start(format_instructions(raw_instructions), debug=debug)
