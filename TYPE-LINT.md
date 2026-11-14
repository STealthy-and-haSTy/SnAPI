# Linting and Type Checking

As a bit of an initial test and foray, this is one of the first packages that
I've created which has linting and type checking support. This is somewhat
experimental, and may or may not remain.

The setup here is intended to work either via the `cli` or via `LSP` packages in
Sublime Text while editing directly. The `cli` is partially intended for the
purposes of potential integration into a `CI/CD` type pipeline.

To incorporate these changes, there are some new control files; these are
marked to not be included in the final package, since they are development-only
files.

The configuration here presumes that the package is intended to support the
Python 3.8 plugin host in addition to the latest Python 3.14+; should we decide
to not allow the older plugin host, more changes could be made here.


## Command line

Create the virtual environment, activate it, and install the required libraries.
Once this is done, you an manually run lint checks:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
ruff check .
```


## Sublime Text LSP

This is tested to work with the following packages:
Install these packages with Package Control:

- `LSP`
- `LSP-ruff`
- `LSP-pyright`

In order for these to work, the `sublime-project` file needs to have this
package as it's top level folder, with the following configuration applied
via `settings`:

```json
{
  "folders": [
    {
      "path": "."
    }
  ],
  "settings": {
    "LSP": {
      "LSP-ruff": {
        "enabled": true,
        "server_path": "auto",
        "initialization_options": {
          "settings.configurationPreference": "filesystemFirst"
        }
      },
      "LSP-pyright": {
        "enabled": true,
        "settings": {
          "pyright.disableTaggedHints": true
        }
      }
    }
  }
}
```

This configuration is intended to make `LSP-ruff` prefer the configuration file
in the root of the project over the internal defaults. That file also disables
`LSP-pyright` from linting; the extra configuration for it here stops the
tagged UI hints that it generates. The goal is ensure that actual lint related
issues are shown only from `Ruff` where possible.
