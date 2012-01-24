import fabric.fabric as dsp
import unittest

class TestBreakpoint(unittest.TestCase):
    def test_small(self):
        # Size 0
        self.assertEqual(dsp.breakpoint([1,2,3,4], 0), [])

        # Size 1-10 with four values
        for s in range(1, 11):
            self.assertEqual(len(dsp.breakpoint([1,2,3,4], s)), s)

            if s > 3:
                self.assertTrue(max(dsp.breakpoint([1,2,3,4], s)) == 4)
                self.assertTrue(min(dsp.breakpoint([1,2,3,4], s)) == 1)

        for s in range(1, 11):
            self.assertEqual(len(dsp.breakpoint([1,['sine',2],3,4], s)), s)

            if s > 3:
                self.assertTrue(max(dsp.breakpoint([1,['sine',2],3,4], s)) == 4)
                self.assertTrue(min(dsp.breakpoint([1,['sine',2],3,4], s)) == 1)

        self.assertTrue(max(dsp.breakpoint([1,2,3,4], 4)) == 4)
        self.assertTrue(min(dsp.breakpoint([1,2,3,4], 4)) == 1)

        self.assertTrue(max(dsp.breakpoint([10,20,30,40], 4)) == 40)
        self.assertTrue(min(dsp.breakpoint([10,20,30,40], 4)) == 10)

    def test_medium(self):
        # Size 40
        self.assertEqual(len(dsp.breakpoint([1,2,3,4], 40)), 40)

class TestUnitConversion(unittest.TestCase):
    def test_conversion(self):
        self.assertEqual(dsp.stf(1), dsp.audio_params[2])
        self.assertEqual(dsp.mstf(1000), dsp.stf(1))
        self.assertEqual(dsp.mstf(1000), dsp.audio_params[2])
        self.assertEqual(dsp.ftms(dsp.mstf(1000)), dsp.mstf(dsp.ftms(1000)))


if __name__ == '__main__':
    unittest.main()
