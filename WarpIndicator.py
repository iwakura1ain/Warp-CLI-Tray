#!/usr/bin/python
import os

from gi import require_version
require_version('Gtk', '3.0')
require_version('AppIndicator3', '0.1')

# requires libayatana-appindicator

from gi.repository import Gtk as gtk, AppIndicator3 as appindicator

import subprocess

# def main():
#     indicator = appindicator.Indicator.new("customtray", "semi-starred-symbolic", appindicator.IndicatorCategory.APPLICATION_STATUS)
#     indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
#     indicator.set_menu(menu())
#     gtk.main()

class WarpIndicator():
    def __init__(self):
        icon = "./yes.svg" if self.get_status() else "./nope.svg"
        
        self.indicator = appindicator.Indicator.new(
            "customtray", icon, appindicator.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.menu())
        
    def menu(self):
        menu = gtk.Menu()

        toggle_warp = gtk.MenuItem('Toggle')
        toggle_warp.connect('activate', self.toggle)
        menu.append(toggle_warp)

        quit_tray = gtk.MenuItem('Exit')
        quit_tray.connect('activate', self.quit)
        menu.append(quit_tray)

        menu.show_all()
        return menu

    def get_status(self):
        status = subprocess.run(['warp-cli', 'status'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        if "Connected" in status:
            return True
        return False
  
    def toggle(self, _):
        if self.get_status():
            subprocess.run(['warp-cli', 'disconnect'])
            self.indicator.set_icon("./nope.svg")
        else:
            subprocess.run(['warp-cli', 'connect'])
            self.indicator.set_icon("./yes.svg")

    def quit(self, _):
        gtk.main_quit()

if __name__ == "__main__":
    WarpIndicator();
    gtk.main()
