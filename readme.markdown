# Fabric 0

Fabric is a computer music system written with the Python v2.x standard library.
It is intended to be used for offline/non-realtime computer music composition. 

It aims to be highly portable, hackable, understandable and powerful. 
Fabric aspires to one day be the Logo of computer music. No big deal!

The system currently implements simple wavetable synthesis and provides tools for
processing sound in the time domain. Frequency domain tools may be added if the 
author learns how that darn FFT works, or when support for pluggable DSP engines 
is implemented in version 3.

# Fabric Roadmap

## Version 1

- Full test coverage
- Standardized install process
- Document install process
- Document template score to show:
    - Loading and manipulating sounds
    - Layering, gain adjustment, basic editing
    - Synthesis and wavetable generation
    - Rendering
- All methods w/at least stub docstring description

## Version 2

- Optimize codebase (find speed bottlenecks and eliminate where possible)
- Fully document source
- First tutorials for the absolute beginner
    - Draw from Miller Puckett's PD book
    - Draw from David Cottle's SC book
    - Draw from FLOSS Manuals PD book
- Expand synthesis capabilities: FM, etc
- Expand 'high level' functionality: compression, reverb?

## Version 3

- First integration with Sugar environment
- Explore csound backend and experimental realtime capabilities
- Explore plugin system for modular synthesis engines (libpd, csound, supercollider, etc)

## Version 4

- Feature complete Sugar integration, GUI environment and render workflow
- Scaffold for ports of Sugar GUI to native Windows/Mac/Linux/Mobile apps

## Version 5

- API freeze
- Full lesson plans for the following age groups:
    - Ages 6 - 8
    - Ages 9 - 11
    - Ages 12 - 15
    - Ages 15+
    - Adults
- Complete support for all major platforms
    - One-click install for Windows, Mac, Linux
    - Full Sugar package
    - Bootable distro
    - Web-based service running on EC2?

