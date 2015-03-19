from copy import deepcopy

from pypot.primitive import LoopPrimitive


class DmpPlayer(LoopPrimitive):
    def __init__(self, robot,
                 motors):

        LoopPrimitive.__init__(self, robot, 50.0)

        self.motors = [getattr(self.robot, m.name) for m in motors]


    def play(self, dmp, duration, repeat, wait):
        if len(self.motors) != dmp.dmps:
            raise ValueError('Must have one dmp per motor!')

        dmp = deepcopy(dmp)

        dmp.timesteps *= repeat
        self.y, _, _ = dmp.rollout()

        self.dt = duration * repeat

        self.start()
        if wait:
            self.wait_to_stop()

    def setup(self):
       for m in self.robot.motors:
            m.compliant = False
            m.pid = (10., 0., 0.)
            m.moving_speed = 0.

    def update(self):
        i = round((self.elapsed_time / self.dt) * len(self.y))

        if i >= len(self.y):
            self.stop()

        else:
            for p, m in zip(self.y[i], self.motors):
                m.goal_position = p

    def teardown(self):
        for m in self.robot.motors:
            m.pid = (4., 0., 0.)
