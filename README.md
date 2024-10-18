[![Tests](https://github.com/science-for-democracy/mapof-elections/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/science-for-democracy/mapof-elections/actions/workflows/python-tests.yml)
[![codecov](https://codecov.io/github/science-for-democracy/mapof-elections/graph/badge.svg?token=EDMLWNYCTP)](https://codecov.io/github/science-for-democracy/mapof-elections)


# Mapof-elections
This pacakge is a plugin for [Mapof](https://pypi.org/project/mapof/) extending
it with capabilities of drawing maps of various election intances.

For the most recent version of Mapof, visit its [git
repo](https://pypi.org/project/mapof/).

> [!WARNING]
> This library contains C++ extensions. Installing it without
> any package manager that uses the PyPi repository requires compiling the C++
> extension from sources. It might be a bit cumbersome as is far beyond the
> scope of this small manual.
 
# Installation
For a simple installation, type
`pip install mapof-elections`
in the console.

For more complicated variants of installation, refer to the readme of mapel
[here](https://github.com/science-for-democracy/mapof).

## Extra dependencies

For the full functionality of the package, it is recommended to also install
extra dependencies executing `pip install mapof-elections[extras]`. The extra
dependencies contain 
```
pulp~=2.5.1
abcvoting~=2.0.0b0
permanent
```  
which unlock approval based committee rules (which require solving I(L)P
programs) and sampling matrices using a permanent-based approach.

# Acknowledgments

This project is part of the [PRAGMA project](https://home.agh.edu.pl/~pragma/)
which has received funding from the [European Research Council
(ERC)](https://home.agh.edu.pl/~pragma/) under the European Union’s Horizon 2020
research and innovation programme ([grant agreement No
101002854](https://erc.easme-web.eu/?p=101002854)).



