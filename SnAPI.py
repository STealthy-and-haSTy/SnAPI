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
        topic = None
        if self.view.match_selector(0, "source.python"):
            extract = self.view.sel()[0]
            if extract.empty():
                extract = self.view.expand_by_class(extract,
                    sublime.CLASS_WORD_START | sublime.CLASS_WORD_END)
            topic = self.view.substr(extract)

            pkg_info = help_index_list().get("SnAPI")
            if lookup_help_topic(pkg_info, topic):
                return sublime.run_command("hyperhelp_topic", {
                    "package": "SnAPI",
                    "topic": topic
                })

        sublime.run_command("hyperhelp_index", {"package": "SnAPI"})
        if topic is not None:
            self.view.window().run_command("insert", {"characters": topic})

    def is_enabled(self):
        return "SnAPI" in help_index_list()


###----------------------------------------------------------------------------
