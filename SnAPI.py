import sublime
import sublime_plugin

from hyperhelp.core import help_index_list, lookup_help_topic


###----------------------------------------------------------------------------


class SnapiLookupCommand(sublime_plugin.TextCommand):
    """
    Open the SnAPI index to browse topics.

    If invoked from a python source file, this will use either the symbol under
    the cursor or the current selection to pre-filter the index to matching
    entries.
    """
    def run(self, edit):
        # For unknown files, open the default topic for a default package.
        #
        # TODO: Should be user configurable?
        if not self.is_build() and not self.is_plugin():
            return sublime.run_command(
                "hyperhelp_topic", {"package": "SublimeAPI"})

        # Get the help index for the type of file currently focused.
        if self.is_plugin():
            pkg_info = help_index_list().get("SublimeAPI")
        else:
            pkg_info = help_index_list().get("SublimeBuild")

        # Get an initial topic; the selected text or the word under the cursor.
        extract = self.view.sel()[0]
        if extract.empty():
            extract = self.view.expand_by_class(extract,
                sublime.CLASS_WORD_START | sublime.CLASS_WORD_END)
        topic = self.view.substr(extract)

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


    def is_plugin(self):
        # Could also ensure the file exists in a Package.
        return self.view.match_selector(0, "source.python")

    def is_build(self):
        name = self.view.name()
        if self.view.file_name() is not None:
            name = self.view.file_name()

        return name.endswith(".sublime-build")

    def is_enabled(self):
        if self.is_build():
            return "SublimeBuild" in help_index_list()

        # For plugins and the default case
        return "SublimeAPI" in help_index_list()


###----------------------------------------------------------------------------
