# wentelx87
Wentel consists of, at the basic level, a memory pointer and an instruction pointer. Instructions are stored loaded into memory. The execution pointer moves to the right after executing the instruction at that memory pointer.

The program is loaded into rightmost slot of memory. For example, if your program is `0010 0000 0101 0100`, 
then the virtual machine will look like this when started:
```
0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0010 0000 0101 0100 (memory)
                                                            ^                   (execution pointer)
^                                                                               (memory pointer)
```



## Opcodes

*Note:* This Wentel Virtual Machine is 8 bit. That is, memory pointers are 8 bits long. Each memory register holds four bits of information. These instructions can be modified to adjust the memory table size.

**`0000`** - no-op

**`0001`** - if the current address's value is equal to the value stored by the adress defined by the next 8 bits, move the execution pointer to the address pointed to by the ninth to the sixteenth bits after the current address.

**`0010`** - move memory pointer to address specified by next 8 bits

**`0011`** - deposit the current address of the execution pointer into the current memory address

**`0100`** - increment current memory address

**`0101`** - decrement current memory address

**`0110`** - move memory pointer left

**`0111`** - move memory pointer right


Invalid opcodes cause undefined behavior. 

## Output

*Note:* Output is not a part of the barebones Wentel specification. Output is instead an 
extension that exploits the unused opcodes in the barebones Wentel specification.

Output is defined by special opcodes. All **`1XXX`** opcodes maniuplate external resources.

**`1000`** - output `0`

**`1001`** - output `1`

In this implementation of the Wentel Virtual Machine, 
every 8 bits it will decode the last 8 bits and output them as ASCII. Escape characters are supported.

## Examples
*Spaces were added to help reading. The Wentel Virtual Machine does not accept spaces.*

`0000 1111 1111 0000 1000` - this snippet will move the execution pointer to `0000 1000` if the curent value is equal to the value pointed to by `1111 1111`

