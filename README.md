# GICS
This library provides a way to parse, manipulate and analyze [GICS](https: #en.wikipedia.org/wiki/Global_Industry_Classification_Standard) codes. GICS (Global Industry Classification Standard) is a classification system by [MSCI](https: #www.msci.com/gics)

## Installation
```
pip install gics
```
## Usage
In practice, GICS codes are represented by strings (just as dates can be). This library provides a wrapper for the string that allows the user to manipulate and display the represented GICS code in different ways.
To wrap a string representing a GICS code, just build a new instance of GICS passing the string as the first argument.

## Example
```python
from gics import GICS

valid_sector_level_GICS = GICS('10')
print(valid_sector_level_GICS.sector.name)  # 'Energy'

valid_full_GICS = GICS('10101010')
print(valid_full_GICS.sector.name)  # 'Energy'
print(valid_full_GICS.sub_industry.name)  # 'Oil & Gas Drilling'
print(valid_full_GICS.level(4).name)  # 'Oil & Gas Drilling'
print(valid_full_GICS.level(3).name)  # 'Energy Equipment & Services'
print(valid_full_GICS.sector.code)  # '10'
```

## GICS API
This section describes every method and property in the GICS object
### Constructor
#### Description
Represents a GICS code. You can instantiate GICS codes using a string representing a code.
The string has to be a valid GICS. If it's not, that isValid method will return false.
Note that creating an empty GICS will mark it as invalid but can still be used to query the definitions (although that object itself will not be a definition)
```
@class      GICS GICS
@param      {string}  code     GICS code to parse. Valid GICS codes are strings 2 to 8 characters long, with even length.
@param      {string}  version  Version of GICS definition to use. By default the latest definition is used. Versions are named after the date in which they became effective, following the format YYYYMMDD. Current available versions are: 20140228 and 20160901 and 20180929 (default).
@throws     {Error}            Throws error if the version is invalid/unsupported.
```
#### Example
```python
from gics import GICS

gics = GICS('4040')  # Default GICS definition version (20160901)
gics_old = GICS('4040', '20140228')  # GICS using a previous definition 
```
### sector
#### Description
Gets the definition for the sector of this GICS object (GICS level 1)
```
@return     {object}  Definition of the GICS level. It has 3 properties: name, description and code. Keep in mind that only level 4 usually has a description.
```
#### Example
```python
from gics import GICS

gics = GICS('1010')
print(gics.sector.name)  # 'Energy'
print(gics.sector.code)  # '10'
```
### industry_group
#### Description
Gets the definition for the industry group of this GICS object (GICS level 1)
```
@return     {object}  Definition of the GICS level. It has 3 properties: name, description and code. Keep in mind that only level 4 usually has a description.
```
#### Example
```python
from gics import GICS

gics = GICS('453010')
print(gics.industry_group.name)  # 'Semiconductors & Semiconductor Equipment'
print(gics.industry_group.code)  # '4530'
 # If asked for a component that's not defined by this level, it returns null
print(gics.sub_industry)  # null
```
### industry
#### Description
Gets the definition for the industry of this GICS object (GICS level 1)
```
@return     {object}  Definition of the GICS level. It has 3 properties: name, description and code. Keep in mind that only level 4 usually has a description.
```
#### Example
```python
from gics import GICS

gics = GICS('453010')
print(gics.industry.name)  # 'Semiconductors & Semiconductor Equipment'
print(gics.industry.code)  # '453010'
```
### sub_industry
#### Description
Gets the definition for the sub-industry of this GICS object (GICS level 1)
```
@return     {object}  Definition of the GICS level. It has 3 properties: name, description and code. Keep in mind that only level 4 usually has a description.
```
#### Example
```python
from gics import GICS

gics = GICS('45301010')
print(gics.sub_industry.name)  # 'Semiconductor Equipment'
print(gics.sub_industry.code)  # '45301010'
print(gics.sub_industry.description)  # 'Manufacturers of semiconductor equipment, including manufacturers of the raw material and equipment used in the solar power industry'
```
### level(gicsLevel)
#### Description
Gets the definition of the given level for this GICS object.
```
@param      {number}  gicsLevel  Level of GICS to get. Valid levels are: 1 (Sector), 2 (Industry Group), 3 (Industry), 4 (Sub-Industry)
```
#### Example
```python
from gics import GICS

gics = GICS('45301010')
print(gics.level(1) == gics.sector)  # true
print(gics.level(2) == gics.industry_group)  # true
print(gics.level(3) == gics.industry)  # true
print(gics.level(4) == gics.sub_industry)  # true
```
### children
#### Description
Gets all the child level elements from this GICS level.
For example, for a Sector level GICS, it will return all Industry Groups in that Sector.
If the GICS is invalid (or empty, as with a null code), it will return all Sectors.
A Sub-industry level GICS will return an empty array.
```
@return     {array} Array containing objects with properties code (the GICS code), name (the name of this GICS), and description (where applicable)
```
#### Example
```python
from gics import GICS

gics = GICS('10')
print(gics.children.length)  # 10
print(gics.children[1].code)  # '1010'
```
### is_same(another_gics)
#### Description
Determines if this GICS is the same as the given one.
To be considered the same both GICS must either be invalid, or be valid and with the exact same code. This means that they represent the same values
at the same level.
```
@param      {object}  another_gics  GICS object to compare with
```
#### Example
```python
from gics import GICS

gics1 = GICS('1010')
gics2 = GICS('1010')
gics1.is_same(gics2)  # true
gics2.is_same(gics1)  # true
```
### is_within(another_gics)
#### Description
Determines if this GICS is a sub-component of the given GICS. For example, GICS 101010 is within GICS 10.
Invalid GICS do not contain any children or belong to any parent, so if any of the GICS are invalid, this will always be false.
Two GICS that are the same are not considered to be within one another (10 does not contain 10).
```
@param      {GICS}  another_gics  GICS object to compare with
```
#### Example
```python
from gics import GICS

GICS('10101010').is_within(GICS('10'))  # true
GICS('101010').is_within(GICS('10'))  # true
GICS('101010').is_within(GICS('1010'))  # true
GICS('1010').is_within(GICS('10'))  # true
GICS('10').is_within(GICS('10'))  # false
GICS('1010').is_within(GICS('1010'))  # false
GICS('invalid').is_within(GICS('10'))  # false
GICS('10').is_within(GICS('invalid'))  # false
GICS('invalid').is_within(GICS('invalid'))  # false
```
### is_immediate_within(another_gics)
#### Description
Determines if this GICS is a sub-component of the given GICS at the most immediate level. For example, GICS 1010 is immediate within GICS 10, but 101010 is not.
Invalid GICS do not contain any children or belong to any parent, so if any of the GICS are invalid, this will always be false.
Two GICS that are the same are not considered to be within one another (10 does not contain 10).
```
@param      {GICS}  another_gics  GICS object to compare with
```
#### Example
```python
from gics import GICS

GICS('10101010').is_immediate_within(GICS('10'))  # false
GICS('101010').is_immediate_within(GICS('10'))  # false
GICS('101010').is_immediate_within(GICS('1010'))  # true
GICS('1010').is_immediate_within(GICS('10'))  # true
GICS('10').is_immediate_within(GICS('10'))  # false
GICS('1010').is_immediate_within(GICS('1010'))  # false
GICS('invalid').is_immediate_within(GICS('10'))  # false
GICS('10').is_immediate_within(GICS('invalid'))  # false
GICS('invalid').is_immediate_within(GICS('invalid'))  # false
```
### contains(another_gics)
#### Description
Determines if this GICS contains the given GICS. For example, GICS 10 contains GICS 101010.
Invalid GICS do not contain any children or belong to any parent, so if any of the GICS are invalid, this will always be false.
Two GICS that are the same are not considered to be within one another (10 does not contain 10).
```
@param      {GICS}  another_gics  GICS object to compare with
```
#### Example
```python
from gics import GICS

GICS('10').contains(GICS('10101010'))  # true
GICS('10').contains(GICS('101010'))  # true
GICS('10').contains(GICS('1010'))  # true
GICS('10').contains(GICS('10'))  # false
GICS('1010').contains(GICS('10'))  # false
GICS('invalid').contains(GICS('10'))  # false
GICS('10').contains(GICS('invalid'))  # false
GICS('invalid').contains(GICS('invalid'))  # false
```
### contains_immediate(another_gics)
#### Description
Determines if this GICS contains the given GICS at the most immediate level. For example, GICS 10 contains immediate GICS 1010, but not 101010.
Invalid GICS do not contain any children or belong to any parent, so if any of the GICS are invalid, this will always be false.
Two GICS that are the same are not considered to be within one another (10 does not contain 10).
```
@param      {GICS}  another_gics  GICS object to compare with
```
#### Example
```python
from gics import GICS

GICS('10').contains_immediate(GICS('10101010'))  # false
GICS('10').contains_immediate(GICS('101010'))  # false
GICS('10').contains_immediate(GICS('1010'))  # true
GICS('10').contains_immediate(GICS('10'))  # false
GICS('1010').contains_immediate(GICS('10'))  # false
GICS('invalid').contains_immediate(GICS('10'))  # false
GICS('10').contains_immediate(GICS('invalid'))  # false
GICS('invalid').contains_immediate(GICS('invalid'))  # false
```