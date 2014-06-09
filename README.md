MagPy
=====

MagPy is a Python 3 library designed to let the user create, use, and analyze the structure of [magmas][1], which includes more specific structures such as monoids and groups. This software is still in prerelease, and the code is very rough, so use at your own risk. This is my first project for a Python library, so any help would be appreciated. 

Features
-----------

* Create magmas by instantiating the abstract base class `magpy.Magma`.
* Compute values and test the properties of magmas.
* Customize the character set used to display the value of magmas, unicode supported.

Planned Features
---------------
 * Full feature compatibility with Maple's [Magma][2] package.
 * Expanding the magma classification system to include more functionality than Maple's Magma package.
 * Symbolic computation with magams, possibly integrating with sympy.
 * Support for algebraic structures with more than one binary operator (rings, fields, etc...).
 * Functions for the bulk parallel processing of magmas of a certian order.
 * Formatted display method for cayley tables.

Installation
--------------

**Linux/Mac**:
```sh
git clone https://github.com/Sintrastes/magpy.git
cd magpy
sudo ./setup.py install
```

Basic Usage
-----------
**Creating a magma**: the Magma class is an abstract class, requiring the abstract properties `cayley_table()`, `order()`, and `magma_set()` to be implemented before using. 

```python
import magpy.magma

class DihedralD3(magpy.Magma):
    CAYLEY_TABLE =[[0,1,2,3,4,5],
                  [1,0,4,5,2,3],
                  [2,5,0,4,3,1],
                  [3,4,5,0,1,2],
                  [4,3,1,2,5,0],
                  [5,2,3,1,0,4]]

```

**Using magma objects**: There are currentley no static methods for determining properties of a magma, so magmas must be instantiated with an object before these methods (like .isGroup()) may be used.

Magmas curentley use `+` as the group operation. Later versions may provide the option of using other operators such as `*` instead.

```python
d = DihedralD3(2)

d.isGroup()
> True

d.isQuandle()
> False

d + d
> 0

d + 3
> 5

```

Version
----

0.1 (prerelease)

License
----

GPL v2


[1]:https://en.wikipedia.org/wiki/Magma_(algebra)
[2]:http://www.maplesoft.com/support/help/Maple/view.aspx?path=Magma
