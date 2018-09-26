import sublime
import sublime_plugin

from hyperhelp.core import help_index_list, lookup_help_topic


###----------------------------------------------------------------------------


class SnapiLookupCommand(sublime_plugin.TextCommand):
    """
    Open the SnAPI index to browse topics.

    Attempts to open the appropriate help topic or package based on the type of
    file being edited and the current selection or text under the cursor.
    """
    def run(self, edit):
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
            extract = self.view.expand_by_class(extract,
                sublime.CLASS_WORD_START | sublime.CLASS_WORD_END)
        topic = self.view.substr(extract).strip()

        # If the initial topic exists, open it directly.
        if lookup_help_topic(pkg_info, topic):
            return sublime.run_command("hyperhelp_topic", {
                "package": pkg_info.package,
                "topic": topic
            })

        # Topic is unknown; open the help index for the package and insert the
        # topic as an initial filter.
        sublime.run_command("hyperhelp_index", {"package": pkg_info.package})
        if topic is not None:
            self.view.window().run_command("insert", {"characters": topic})

    def pkg_for_file(self):
        # Use scope because unsaved plugins don't have a sensible name.
        # For now, all python files are considered plugins.
        if self.view.match_selector(0, "source.python"):
            return "SublimeAPI"

        name = self.view.name()
        if self.view.file_name() is not None:
            name = self.view.file_name()

        if name.endswith(".sublime-build"):
            return "SublimeBuild"

        if name.endswith(".sublime-color-scheme"):
            return "SublimeColorScheme"

        # Unrecognized file type
        return None

    def is_enabled(self):
        pkg = self.pkg_for_file() or "SublimeAPI"
        return pkg in help_index_list()


###----------------------------------------------------------------------------
