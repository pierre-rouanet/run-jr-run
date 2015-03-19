from numpy import array

from pypot.primitive import LoopPrimitive


class Recorder(LoopPrimitive):
    def __init__(self, robot, motors):
        LoopPrimitive.__init__(self, robot, 50.0)

        self.motors = [getattr(self.robot, m.name) for m in motors]

    def setup(self):
        self._traj = []

    def update(self):
        self._traj.append([m.present_position for m in self.motors])

    @property
    def trajectory(self):
        return array(self._traj)
