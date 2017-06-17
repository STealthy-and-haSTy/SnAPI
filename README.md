SnAPI
=====

SnAPI is a simple package that provides a local copy of the Sublime Text 3 [API
documentation](http://www.sublimetext.com/docs/3/api_reference.html) directly
from within Sublime, using the [hyperhelp](https://github.com/OdatNurd/hyperhelp)
help system for navigation.

SnAPI is pronounced "Snappy", as having API documentation readily available from
directly within Sublime keeps you focused on your coding. Also it was a name
suggested to me that stuck in my head. Please blame @kingkeith for suggesting
the name and my brain for latching onto it so completely.

Also, please note that all help text is taken directly from the above linked
official API reference and is Copyright © Sublime HQ Pty Ltd.


-------------------------------------------------------------------------------


**NOTE:** Although there is only help contained within the package, it is still
in active development and as such everything is subject to change.


-------------------------------------------------------------------------------


## Installation ##

SnAPI relies on the [hyperhelp](https://github.com/OdatNurd/hyperhelp)
dependency package to display the actual help. Since the package is not
officially released yet, `hyperhelp` is not in the official list of Sublime
dependencies, and so you must manually install it prior to installing SnAPI.

See the code repository linked above for manual installation instructions. You
can tell if it's installed by checking the Command Palette to see if there are
any commands prefixed by `HyperHelp:`.


### Package Control ###

The best way to install the package is via PackageControl, as this will take
care of ensuring that the package is kept up to date without your having to do
anything at all.

SnAPI is currently not listed in Package Control because it's not officially
released yet. In order to install via Package Control, open the Command Palette
and select the command `Package Control: Add Repository` and then paste in the
URL to this repository (https://github.com/OdatNurd/SnAPI).

Once this is done, you will be able to install the package via the command
palette using the command `Package Control: Install Package` and searching for
`SnAPI`.


### Manual Installation ###

In order to manually install the package, clone the repository into your
Sublime Text `Packages` directory. You can locate this directory by choosing
`Preferences > Browse Packages...` from the menu.

Manual installation is not recommended for most users, as in this case you are
responsible for manually keeping everything up to date. You should only use
manual installation if you have a very compelling reason to do so and are
familiar enough with the process to know how to do it properly.

<!--
If you do a manual install of the package, you must also manually install the
hyperhelp dependency. Optionally you can manually install SnAPI and then
use the `Package Control: Satisfy Dependencies` command to have Package Control
install hyperhelp for you.
-->


-------------------------------------------------------------------------------


## Usage ##

Once installed, the following command will be added to the command palette,
allowing you to directly open the SnAPI help files. In addition you can also
get at the help by choosing the `HyperHelp: List Available Help` command from
the command palette and choosing SnAPI from the list.


### `SnAPI: Sublime API Help` ###

This opens the help system at the root of the API documentation. This is a
quick jumping off point to all of the various sections of the help system.


-------------------------------------------------------------------------------


## Navigating Help ##

SnAPI uses the standard help navigation in
[hyperhelp](https://github.com/OdatNurd/hyperhelp). If you're not familiar with
how the system works, you can select the `HyperHelp: Help on Help` command from
the command palette to get more information.


-------------------------------------------------------------------------------


## License ##

Note that the license below

Note that the license below *DOES NOT* include any of the help files, which are
taken from the official API reference for Sublime Text at
http://www.sublimetext.com/docs/3/api_reference.html and are Copyright ©
Sublime HQ Pty Ltd.

All other content in this package are licensed under the MIT License.

Copyright 2017 Terence Martin

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
