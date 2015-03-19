import os

from poppy.creatures import PoppyErgoJr

from .driveback_arm import DrivebackArm
from .dmp import DmpPlayer, load_dmp
from .record import Recorder


class Env(object):
    def __init__(self):
        bp = os.path.join(os.path.dirname(__file__), 'driveback_arm')
        self.arm = DrivebackArm(base_path=bp)

        self.jr = PoppyErgoJr()
        motors = [getattr(self.jr, 'm{}'.format(i)) for i in [2, 3, 5, 6]]
        self.dmp_player = DmpPlayer(self.jr, motors)

        filename = os.path.join(os.path.dirname(__file__), 'dmp', 'base_dmp.json')
        with open(filename) as f:
            self.base_dmp = load_dmp(f)

        self.recorder = Recorder(self.jr, motors)

    def setup(self):
        for m in self.arm.motors:
            m.compliant = False
            m.torque_limit = 75.

        for m in self.jr.motors:
            m.compliant = False
            m.torque_limit = 100.

        self.jr.jump.setup()
        self.drive_back()

    def teardown(self):
        self.arm.close()
        self.jr.close()

    def drive_back(self):
        self.jr.goto_position(self.jr.jump.down, 1, wait=True)

        self.jr.m3.goal_position = 150
        self.jr.m6.goal_position = 30

        for __ in range(2):
            self.arm.driveback.start()
            self.arm.driveback.wait_to_stop()

        for m in self.jr.motors:
            m.compliant = False

        self.jr.goto_position(self.jr.jump.down, 1, wait=True)
