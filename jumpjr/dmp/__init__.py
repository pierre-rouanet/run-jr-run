import json
import numpy

from pydmps.dmp_discrete import DMPs_discrete
from pydmps.dmp_rhythmic import DMPs_rhythmic


from player import DmpPlayer


class NumpyAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def save_dmp(dmp, f):
    data = {
        'type': 'discrete' if isinstance(dmp, DMPs_discrete) else 'rhythmic',
        'dmps': dmp.dmps,
        'bfs': dmp.bfs,
        'dt': dmp.dt,
        'y0': dmp.y0,
        'goal': dmp.goal,
        'w': dmp.w,
        'ay': dmp.ay,
        'by': dmp.by,
        }

    json.dump(data, f, cls=NumpyAwareJSONEncoder)

def load_dmp(f):
    data = json.load(f)

    dmp_cls = DMPs_discrete if data.pop('type') == 'discrete' else DMPs_rhythmic

    kwargs = {k: numpy.array(v) if isinstance(v, list) else v
              for k, v in data.items()}

    return dmp_cls(**kwargs)
