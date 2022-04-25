
# SLAAD
### Simple Lua AutomAtic Disassembler

SLAAD is a Lua bytecode disassembler targeting Lua 5.4.4. 
It has the ability to disassemble lua bytecode files into its VM instructions, and can label instructions with the operation they perform.

No relation to a different [Slaad](https://forgottenrealms.fandom.com/wiki/Slaad) you may have heard about.

## Usage
```
usage: Disassemble a Lua 5.4.4 bytecode file [-h] [-v] [-vv] [-op] <file>

positional arguments:
  <file>               The file to be disassembled

options:
  -h, --help           show this help message and exit
  -v, --verbose        Verbose (print significant data member parsed)
  -vv, --very-verbose  Very Verbose (print all data member parsed)
  -op, --opcode-notes  Print notes for each opcode to describe its operation
```

## Instruction Syntax Notes
From Lua source code:
```
R[x] - register
K[x] - constant (in constant table)
RK(x) == if k(i) then K[x] else R[x]
```

## Sources
* [The Lua reference manual](https://www.lua.org/manual/5.4/)
* [The Lua Source Code](https://www.lua.org/source/5.4/)

* __A No-Frills Introduction to Lua 5.1 VM Instructions__
  * by Kein-Hong Man, esq. <khman AT users.sf.net>

The Lua sources were used for obvious reasons, the No-Frills Introduction to Lua 5.1 was used to get me started in the right direction with this project. Lua has had some significant under-the-hood changes since 5.1, so I didn't actually make too much use of that source.

