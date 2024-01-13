#
# This file is part of the "IDARustCargo" project
# The MIT License - See "LICENSE" for license information.
#

import idautils
import idaapi
import re


def remove_duplicates(items):
    unique_items = []
    seen = set()
    for item in items:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)
    return unique_items


class RustCargoChooser(idaapi.Choose):
    def __init__(self, title, items):
        print("RustCargoChooser init")
        idaapi.Choose.__init__(self, title, [
            ["Registry", 15],
            ["Crate", 25],
            ["Version", 10]
        ])
        self.items = items
        
    def OnGetSize(self):
        return len(self.items)

    def OnGetLine(self, n):
        return self.items[n]

    def OnSelectLine(self, n):
        pass


class IDARustCargo():
    def __init__(self):
        print("IDARustCargo init")
        self.pattern = re.compile(r"[\/\\]registry[\/\\]src[\/\\]([a-z]+\.[a-z]+\.[a-z]+)-[a-z0-9]+[\/\\]([a-z0-9-_]+)-([0-9]+\.[0-9]+\.[0-9]+)")
        items = self.process_strings()
        self.chooser = RustCargoChooser("Cargo Packages", items)
        self.chooser.Show()
        
    def process_strings(self):
        items = []
        for string in idautils.Strings():
            match = self.pattern.search(str(string))
            if match:
                items.append(match.groups())
        res = remove_duplicates(items)
        return res


class IDARustCargoPlugin(idaapi.plugin_t):
    PLUGIN_NAME = "IDA Rust Cargo Package Dumper"
    PLUGIN_DIRECTORY = "IDARustCargo"
    PLUGIN_DESCRIPTION = "Display potentially installed Cargo packages from compiled binary"

    flags = idaapi.PLUGIN_UNL
    comment = PLUGIN_DESCRIPTION
    help = PLUGIN_DESCRIPTION
    wanted_name = PLUGIN_NAME
    wanted_hotkey = ""

    def init(self):
        return idaapi.PLUGIN_OK

    def run(self, arg):
        self.r = IDARustCargo()
        return 1

    def term(self):
        pass


def PLUGIN_ENTRY():
    return IDARustCargoPlugin()
