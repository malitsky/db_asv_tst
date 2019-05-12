# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

import time as ttime
import uuid

# from databroker.headersource.mongo import MDS
# from databroker.utils import create_test_database
# from databroker.mongo import Registry

from databroker.tests.utils import build_pymongo_backed_broker
from databroker.tests.test_mds import (setup_syn, syn_data)


class Request:

    def addfinalizer(self, f):
        pass


class DatabrokerSuite:

    db = None
    mds_all = None
	
    def setup(self):
        request = Request()
        self.db = build_pymongo_backed_broker(request)
        self.mds_all = self.db.mds


    def time_bulk_insert(self):
        mdsc = self.mds_all
        num = 50
        rs, e_desc, data_keys = setup_syn(mdsc)
        all_data = syn_data(data_keys, num)

        mdsc.bulk_insert_events(e_desc, all_data, validate=False)
        mdsc.insert_run_stop(rs, ttime.time(), uid=str(uuid.uuid4()))

        '''
        ev_gen = mdsc.get_events_generator(e_desc)

        for ret, expt in zip(ev_gen, all_data):
            assert ret['descriptor'] == e_desc
            for k in ['data', 'timestamps', 'time', 'uid', 'seq_num']:
                print(k, ret[k])
                assert ret[k] == expt[k]
            assert ret['filled'] == {'Z': False}
        '''

