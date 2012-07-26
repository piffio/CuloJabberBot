import transmissionrpc
import ConfigParser
import urllib
import logging


class TransmissionClient:
    def __init__(self, config, init_list=False):
        self.tc = None
        self.torrent_list = None

        self._host = config.get('Transmission', 'host')
        self._port = config.getint('Transmission', 'port')
        self._user = config.get('Transmission', 'user')
        self._passwd = config.get('Transmission', 'passwd')

        print 'Connecting to ' + self._host

        # Create a Client instance
        self.tc = transmissionrpc.Client(address=self._host,
                port=self._port,
                user=self._user,
                password=self._passwd)

        logging.getLogger('transmissionrpc').setLevel(logging.DEBUG)

        # Initialize the torrent list
        if (init_list is True):
            self.update_torrent_list()

    ##
    # Private Methods
    ##
    def __get_list(self):
        return self.torrent_list

    def __format_out_str(self, dict_info, detailed = False):
        out = ""
        for id in dict_info:
            out += str(id) + '\t' + dict_info[id].name + \
                    '\t' + dict_info[id].status + \
                    '\t' + str(dict_info[id].progress) + '%'
            if detailed == True:
                out += '\n\tRatio: ' + str(dict_info[id].ratio)
                out += '\n\tDate Added: ' + str(dict_info[id].date_added)
                if int(dict_info[id].progress) == 100:
                    out += '\n\tDate Done: ' + str(dict_info[id].date_done)
                else:
                    out += '\n\tETA: ' + str(dict_info[id].eta)
            out += '\n' 
        return out

    ##
    # Public Interface
    ##
    def update_torrent_list(self):
        self.torrent_list = self.tc.list()

    def get_torrent_info(self, ids):
        info = self.tc.info(ids)
        return self.__format_out_str(info, detailed = True)

    def get_list_str(self):
        list_dict = self.__get_list()
        return self.__format_out_str(list_dict)

    def stop(self, ids):
        self.tc.stop(ids)
        return self.__format_out_str(self.tc.info(ids))

    def start(self, ids):
        self.tc.start(ids)
        return self.__format_out_str(self.tc.info(ids))

    def remove_torrent(self, ids, delete_data = False):
        self.tc.remove(ids, delete_data)
        return self.get_list_str()

    def add_torrent(self, uri):
        decoded_uri = urllib.unquote_plus(uri)
        try:
            self.tc.add_uri(uri)
        except transmissionrpc.TransmissionError:
            return "An error has occurred, check log files"
        finally:
            return self.get_list_str()


# Test the class interface
if __name__ == '__main__':
    # Test the interface
    config = ConfigParser.ConfigParser()
    config.read('culojabberbot.conf')

    trans_cl = TransmissionClient(config=config, init_list=True)

    mylist = trans_cl.get_list_str()
    print "Dumping torrent list"
    print mylist

    torrent_info = trans_cl.get_torrent_info('12')
    print "Dumping torrent information"
    print torrent_info

# End
# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4
