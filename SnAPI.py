import sublime
import sublime_plugin

import textwrap
import os


###----------------------------------------------------------------------------


_scope_map = {
    # Default scope.
    "source.python": "SublimeAPI",

    # Enhanced scopes provided by PackageDev; Sublime packages use source.json
    # which is not unique enough.
    "source.json.sublime.build": "SublimeBuild",
    "source.json.sublime.color-scheme": "SublimeColorScheme"
}

_extension_map = {
    ".py": "SublimeAPI",

    ".sublime-build": "SublimeBuild",
    ".sublime-color-scheme": "SublimeColorScheme"
}



###----------------------------------------------------------------------------


def _is_hh_enabled():
    """
    A simple function which determines if HyperHelp is currently an available
    package in the system. This is done by checking to see if its Help index is
    available or not.

    The return value is True if HyperHelp is installed and available, and False
    otherwise.

    Note that if HyperHelp is installed but in ignored_packages, this will
    return False even though imports of functionality from within it will still
    function as expected.
    """
    return bool([res for res in sublime.find_resources('hyperhelp.json')
                 if "/HyperHelp/" in res])


###----------------------------------------------------------------------------


def plugin_loaded():
    """
    SnAPI is a simplistic package; however in order for its commands to work
    as expected, HyperHelp needs to be installed.

    Here we check to see if it is, and if it is not, display a message.

    We don't stop the package from loading, since we are only going to invoke
    commands, and those will just be missing.
    """
    if not _is_hh_enabled():
        sublime.message_dialog(textwrap.dedent("""
            SnAPI requires the HyperHelp package to be installed in order to
            display its help content.

            Please install HyperHelp from Package Control.
        """))


###----------------------------------------------------------------------------


def _word_under_cursor(view):
    """
    Get the word under the cursor, if possible. The caret must be either in a
    word or at the start of a word boundary for this to work; if the caret is
    anywhere else, no word will be returned.

    This uses the word separators from the view settings in the given view but
    also adds in whitespace characters, since those also separate words but are
    generally not included in the setting.
    """
    if len(view.sel()) == 1:
        word_class = sublime.CLASS_WORD_START | sublime.CLASS_WORD_END
        sep = view.settings().get("word_separators", "") + " \t\n"

        pt = view.sel()[0].begin()
        pt_class = view.classify(pt)

        if view.substr(pt) in sep:
            return None

        if pt_class & sublime.CLASS_WORD_START == 0:
            word = view.expand_by_class(pt, word_class, sep)
        else:
            if view.substr(pt+1) in sep:
                word = sublime.Region(pt, pt + 1)
            else:
                word = view.expand_by_class(pt + 1, word_class, sep)

        return view.substr(word)

    return None


class SnapiLookupCommand(sublime_plugin.TextCommand):
    """
    Open the SnAPI index to browse topics.

    Attempts to open the appropriate help topic or package based on the type of
    file being edited and the current selection or text under the cursor.
    """
    def run(self, edit):
        # Lazy import the functions that we need
        from HyperHelp.helpcore.core import help_index_list, lookup_help_topic

        pkg_name = self.pkg_for_file()

        # For unknown files, open the default topic for a default package.
        #
        # TODO: Should be user configurable?
        if pkg_name is None:
            return sublime.run_command(
                "hyperhelp_topic", {"package": "SublimeAPI"})

        # Get the help index for the type of file currently focused.
        pkg_info = help_index_list().get(pkg_name)

        # Get an initial topic; the selected text or the word under the cursor.
        extract = self.view.sel()[0]
        if extract.empty():
            topic = _word_under_cursor(self.view)
        else:
            topic = self.view.substr(extract)

        # If the initial topic exists and is unique, open it directly.
        if topic and lookup_help_topic(pkg_info, topic):
            return sublime.run_command("hyperhelp_topic", {
                "package": pkg_info.package,
                "topic": topic
            })

        # Open the root of the help package if the topic is empty, or open the
        # index popup if it has some text. In the latter case, also use it as
        # the default filter so the user can self disambiguate.
        sublime.run_command("hyperhelp_index" if topic else "hyperhelp_topic",
                            {"package": pkg_info.package})
        if topic:
            self.view.window().run_command("insert", {"characters": topic})

    def pkg_for_file(self):
        # Use scope if possible to try and catch unsaved files.
        for scope, pkg in _scope_map.items():
            if self.view.match_selector(0, scope):
                return pkg

        # Fall back to using the extension on the file.
        name = self.view.name() or self.view.file_name() or ""
        ext = os.path.splitext(name)[1]

        for extension, pkg in _extension_map.items():
            if ext == extension:
                return pkg

        # Unrecognized file type
        return None

    def is_enabled(self):
        if not _is_hh_enabled():
            return False

        # Lazy import the lookup function, then find the package that we should
        # be displaying help for and, if we have help for it, we are good.
        from HyperHelp.helpcore.core import help_index_list

        pkg = self.pkg_for_file() or "SublimeAPI"
        return pkg in help_index_list()


###----------------------------------------------------------------------------
