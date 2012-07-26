import transmissionrpc


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

        # Initialize the torrent list
        if (init_list is True):
            self.update_torrent_list()

    def update_torrent_list(self):
        self.torrent_list = self.tc.list()

    def get_list(self):
        return self.torrent_list

    def stop(self, ids):
        self.tc.stop(ids)
        return self.tc.info(ids)

    def start(self, ids):
        self.tc.start(ids)
        return self.tc.info(ids)

# Test the class interface
if __name__ == '__main__':
    trans_cl = TransmissionClient(init_list=True)
    mylist = trans_cl.get_list()

    print mylist

# End
# vim: expandtab tabstop=4 shiftwidth=4 softtabstop=4
