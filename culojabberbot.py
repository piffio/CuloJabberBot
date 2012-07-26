#!/usr/bin/python
#
# culobot.py: Culo JabberBot
#             A versatile jabber bot that can control a transmission server,
#             give you informations about the host where it's running, and
#             maybe more in the future
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import sys
import transmissionrpc
import logging
import ConfigParser

from jabberbot import *
from transmissionclient import *


class CuloBot(JabberBot):
    def __init__(self, *args, **kwargs):
        # Initialize some data
        self._debug = False
        self.torrent_list = None
        self.config = ConfigParser.ConfigParser()
        self.config.read('culojabberbot.conf')

        # Global configuration first
        self._debug = self.config.getboolean('Main', 'debug')

        # Jabber auth configuration
        domain = self.config.get('Jabber', 'domain')
        user = self.config.get('Jabber', 'user')
        
        if len(domain) > 0:
            self._user = user + '@' + domain
        else:
            seld._user = user

        self._passwd = self.config.get('Jabber', 'pass')

        # Chatroom configuration
        conf_domain = self.config.get('Jabber', 'conference_domain')
        chatroom = self.config.get('Jabber', 'chatroom')

        if len(conf_domain) > 0:
            self._chatroom = chatroom + '@' + conf_domain
        else:
            self._chatroom = chatroom

        self._chat_autoconn = self.config.getboolean('Jabber', 'chatroom_autoconnect')

        self.__prepend = '\n'
        self.__append = None

        # Create the Jabber client
        super(CuloBot, self).__init__(username=self._user,
                password=self._passwd,
                debug=self._debug)

        # Create the transmission client
        self.tc = TransmissionClient(config=self.config,
                init_list=True)



    ###
    # Private Methods
    ###
    def __format_message(self, msg):
        tmp_msg = ""
        if self.__prepend:
            tmp_msg += self.__prepend
        tmp_msg += msg
        if self.__append:
            tmp_msg += self.__append
        return tmp_msg


    ####################
    # Jabber Interface #
    ####################

    ###
    # System Commands
    ###
    # Uptime command
    @botcmd
    def sys_uptime(self, mess, args):
        """Get current uptime information"""
        return subprocess.check_output('uptime')

    # Get free space on the host
    @botcmd
    def sys_space(self, mess, args):
        """Get informations about disk usage on the host
        running the bot"""
        return subprocess.check_output(['df', '-h'])

    @botcmd
    def sys_mem(self, mess, args):
        """Get informations about the memory usage on the host
        """
        return subprocess.check_output(['free'])

    @botcmd
    def sys_w(self, mess, args):
        """Who is currently connected on the host running the bot?"""
        return subprocess.check_output('w')

    ###
    # Interaction Commands
    ###
    # Culo command
    @botcmd
    def culo(self, mess, args):
        """Culo"""
        return 'Mavaffanculo!'

    # Join the chatroom
    @botcmd
    def join_chat(self, mess, args):
        self.muc_join_room(self._chatroom)
        return "Joined room " + self._chatroom

    # Leave the chatroom
    @botcmd
    def leave_chat(self, mess, args):
        self.muc_part_room(self._chatroom)
        return "Left room " + self._chatroom


    ###
    # Transmission Commands
    ###

    # List command
    @botcmd
    def tor_list(self, mess, args):
        """List torrents"""
        self.tc.update_torrent_list()
        return self.__format_message(self.tc.get_list_str())

    # Show details on a torrent
    @botcmd
    def tor_info(self, mess, args):
        return self.__format_message(self.tc.get_torrent_info(args))

    @botcmd
    def tor_pause(self, mess, args):
        return self.__format_message(self.tc.stop(args))

    @botcmd
    def tor_start(self, mess, args):
        return self.__format_message(self.tc.start(args))

    @botcmd
    def tor_remove(self, mess, args):
        return self.__format_message(self.tc.remove_torrent(args))

    @botcmd
    def tor_remove_data(self, mess, args):
        return self.__format_message(self.tc.remove_torrent(args, True))

    @botcmd
    def tor_add(self, mess, args):
        return self.__format_message(self.tc.add_torrent(args))

# Init
if __name__ == '__main__':
    logging.basicConfig()
    culobot = CuloBot()
    culobot.serve_forever()

# End
# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4
