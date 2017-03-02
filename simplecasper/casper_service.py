from devp2p.service import WiredService
from casper_protocol import CasperProtocol
from ethereum import slogging

log = slogging.get_logger('casper')


class CasperService(WiredService):

    name = 'casper'
    default_config = dict(
    )

    # required by WiredService
    wire_protocol = CasperProtocol  # create for each peer

    def __init__(self, app):
        self.config = app.config['casper']
        self.db = app.services.db

        if 'network_id' in self.db:
            db_network_id = self.db.get('network_id')
            if db_network_id != str(self.config['network_id']):
                raise RuntimeError(
                    "The database in '{}' was initialized with network id {} and can not be used "
                    "when connecting to network id {}. Please choose a different data directory.".format(
                        self.config['db']['data_dir'], db_network_id, self.config['network_id']
                    )
                )
        else:
            self.db.put('network_id', str(self.config['network_id']))
            self.db.commit()

        super(CasperService, self).__init__(app)

    def on_wire_protocol_start(self, proto):
        log.debug('----------------------------------')
        log.debug('on_wire_protocol_start', proto=proto)
        assert isinstance(proto, self.wire_protocol)
        # register callbacks
        proto.receive_status_callbacks.append(self.on_receive_status)
        proto.receive_prepare_callbacks.append(self.on_receive_prepare)
        proto.receive_commit_callbacks.append(self.on_receive_commit)

        # TODO: send status
        status_mock = (0, '', '')
        proto.send_status(chain_difficulty=status_mock[0],
                          chain_head_hash=status_mock[1],
                          genesis_hash=status_mock[2])

    def on_wire_protocol_stop(self, proto):
        assert isinstance(proto, self.wire_protocol)
        log.debug('----------------------------------')
        log.debug('on_wire_protocol_stop', proto=proto)

    def on_receive_status(self, csp_version, network_id, chain_difficulty, chain_head_hash, genesis_hash):
        pass

    def on_receive_prepare(self, hash, view, view_source):
        pass

    def on_receive_commit(self, hash, view):
        pass