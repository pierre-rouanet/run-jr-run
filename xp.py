import time

from driveback_arm import DrivebackArm
from poppy.creatures import PoppyErgoJr

if __name__ == '__main__':
    arm = DrivebackArm()
    print('DriveBack Arm created')

    jr = PoppyErgoJr()
    print('Poppy Ergo Jr created')

    arm.driveback.start()
    arm.driveback.wait_to_stop()

    for m in jr.motors:
        m.torque_limit = 100.

    for _ in range(15):
        jr.jump.start()
        time.sleep(5)
        jr.jump.stop()

        time.sleep(1)

        jr.m3.goal_position = 150
        jr.m6.goal_position = 30

        for __ in range(2):
            arm.driveback.start()
            arm.driveback.wait_to_stop()

        for m in jr.motors:
            m.compliant = False

        jr.goto_position(jr.jump.down, 1, wait=True)

    arm.close()
    jr.close()
