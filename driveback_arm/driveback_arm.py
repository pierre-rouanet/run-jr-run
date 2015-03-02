import time

from poppy.creatures import AbstractPoppyCreature
from pypot.primitive import Primitive


class DriveBack(Primitive):
    def setup(self):
        for m in self.robot.motors:
            m.compliant = False
            m.moving_speed = 0
            m.torque_limit = 75.

        self.robot.arm.goto_position(-75, 1, wait=True)

    def run(self):
        self.robot.arm.goto_position(55, 1, wait=True)

        # Wait for stabilization
        self.robot.arm.torque_limit = 25.
        time.sleep(1.)

        self.robot.arm.goto_position(-75, 1, wait=True)

    def teardown(self):
        for m in self.robot.motors:
            m.compliant = True


class DrivebackArm(AbstractPoppyCreature):
    @classmethod
    def setup(cls, robot):
        robot.attach_primitive(DriveBack(robot), 'driveback')
