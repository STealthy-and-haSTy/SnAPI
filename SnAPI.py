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
        # Jump directly to the build system documentation in builds.
        if self.is_build():
            return sublime.run_command("hyperhelp_topic", {
                "package": "SublimeBuild",
                "topic": "index.txt"
            })

        # In plugin files, try to zero in on the topic under the cursor or in
        # the selection.
        topic = None
        if self.is_plugin():
            extract = self.view.sel()[0]
            if extract.empty():
                extract = self.view.expand_by_class(extract,
                    sublime.CLASS_WORD_START | sublime.CLASS_WORD_END)
            topic = self.view.substr(extract)

            pkg_info = help_index_list().get("SublimeAPI")
            if lookup_help_topic(pkg_info, topic):
                return sublime.run_command("hyperhelp_topic", {
                    "package": "SublimeAPI",
                    "topic": topic
                })

        # Open the API help by default, optionally also using the topic
        # selected above.
        sublime.run_command("hyperhelp_index", {"package": "SublimeAPI"})
        if topic is not None:
            self.view.window().run_command("insert", {"characters": topic})

    def is_plugin(self):
        return self.view.match_selector(0, "source.python")

    def is_build(self):
        name = self.view.name()
        if self.view.file_name() is not None:
            name = self.view.file_name()

        return name.endswith(".sublime-build")

    def is_enabled(self):
        return all(key in help_index_list() for key in (
            "SublimeAPI",
            "SublimeBuild"
        ))


###----------------------------------------------------------------------------
