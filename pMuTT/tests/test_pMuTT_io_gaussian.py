import unittest
import os
import numpy as np
from pMuTT.io_ import gaussian

test_file = os.path.join(os.path.dirname(__file__), 'test_gaussian.log')


class TestGaussian(unittest.TestCase):
    def test_read_zpe(self):
        self.assertAlmostEqual(gaussian.read_zpe(test_file), 0.451590)

    def test_read_electronic_and_zpe(self):
        self.assertAlmostEqual(gaussian.read_electronic_and_zpe(test_file),
                               -31835.216711)

    def test_read_freq(self):
        expected_freq = np.array([
            27.8123, 47.5709, 54.1668, 63.3422, 70.3570, 83.5806,
            105.7893, 106.3834, 110.1717, 118.9769, 128.5087, 131.6157,
            139.4795, 144.8822, 148.6762, 150.7479, 158.0838, 162.6256,
            167.1256, 168.3303, 173.9985, 178.1156, 188.6688, 192.7570,
            198.7537, 203.8342, 206.0958, 206.9989, 220.1416, 223.4077,
            224.4668, 228.7312, 231.6316, 240.6201, 252.2056, 255.3178,
            263.2650, 264.7325, 265.8385, 266.4317, 269.3429, 271.3071,
            277.1693, 280.3887, 284.9428, 290.9176, 295.4862, 298.4597,
            303.3893, 309.2622, 312.9840, 315.8913, 318.1305, 319.7522,
            321.2753, 322.4733, 326.9842, 333.4541, 340.0401, 345.5120,
            348.0656, 350.8158, 353.0702, 353.6111, 356.1007, 357.6536,
            359.2877, 367.0172, 369.3855, 369.8407, 371.1798, 374.0695,
            374.6035, 376.8763, 377.6512, 380.5837, 386.9291, 388.8287,
            390.1100, 395.3614, 398.0700, 403.8377, 404.0733, 406.3628,
            410.7360, 413.7586, 419.0988, 420.4172, 422.7343, 433.6646,
            440.4825, 442.7119, 444.4128, 446.2963, 455.4076, 465.6478,
            474.9199, 475.4469, 482.6803, 482.7576, 488.8146, 491.5016,
            501.5024, 504.8515, 511.2423, 516.6283, 526.2766, 535.2972,
            558.6641, 570.2303, 577.7282, 579.9795, 581.9509, 589.6657,
            593.8711, 604.6950, 605.9620, 652.3132, 663.5726, 666.5601,
            669.5307, 680.1766, 694.5581, 718.8642, 721.0991, 721.6467,
            730.9165, 734.4614, 738.8954, 739.2874, 744.5907, 747.6314,
            752.4637, 754.0269, 754.7830, 760.8011, 765.1364, 767.2267,
            767.9609, 772.7335, 775.1048, 776.9790, 778.1853, 780.4696,
            782.4896, 784.6325, 792.9234, 796.1776, 800.2807, 809.2837,
            810.2514, 812.6860, 815.0878, 816.1694, 818.6536, 822.8071,
            823.8286, 826.6099, 829.4161, 832.3744, 836.4288, 837.7248,
            850.0946, 850.5175, 853.2736, 854.5033, 857.6854, 858.5265,
            860.3740, 865.7335, 866.7068, 887.7243, 924.0169, 927.7069,
            931.9097, 950.7322, 955.9708, 971.7114, 979.8923, 980.4738,
            1007.0644, 1017.2820, 1042.7275, 1063.6456, 1068.8569, 1093.0158,
            1101.6547, 1124.3030, 1125.2714, 1129.4260, 1135.0911, 1138.0975,
            1141.8434, 1147.9123, 1148.0797, 1152.3754, 1157.5488, 1162.5875,
            1168.5421, 1170.1698, 1175.7276, 1180.3671, 1191.7226, 1197.5352,
            1201.7893, 1202.9845, 1206.5067, 1206.8160, 1209.8491, 1212.5965,
            1215.9923, 1216.9741, 1217.3988, 1225.6334, 1231.5981, 1233.0540,
            1242.0423, 1244.3377, 1246.8269, 1248.8556, 1255.7530, 1258.2321,
            1268.6540, 1273.0555, 1279.0952, 1290.6498, 1330.7360, 1333.6738,
            1348.6979, 1350.5632, 1392.6681, 1425.2621, 1485.7062, 1497.9658,
            1525.1034, 1536.7057, 2620.6126, 2695.6448, 3054.4311, 3068.2387,
            3074.8332, 3111.5420, 3121.8378, 3131.6155, 3149.3723, 3177.2311,
            3179.1266, 3617.1548, 3666.5503])
        np.testing.assert_array_almost_equal(np.array(gaussian.read_frequencies(test_file)),
                                             expected_freq)

    def test_rotational_temperatures(self):
        expected_rot_temp = np.array([0.00005, 0.00004, 0.00004])
        np.testing.assert_array_almost_equal(np.array(gaussian.read_rotational_temperatures(test_file)),
                                             expected_rot_temp)

    def test_read_molecular_mass(self):
        self.assertAlmostEqual(gaussian.read_molecular_mass(test_file),
                               8470.11614)

    def test_rot_symmetry_number(self):
        self.assertEqual(gaussian.read_rot_symmetry_num(test_file), 1)


if __name__ == '__main__':
    unittest.main()