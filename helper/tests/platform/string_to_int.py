# -*- coding: utf-8 -*-
import unittest
from helper.platform.data_helper import unify_string


class StringToIntTest(unittest.TestCase):

    def test_convert_string_to_int(self):
        actual = unify_string("hellтіo world")
        expected = '9L1PXL8KPbIR3'
        self.assertEquals(expected, actual)

        actual = unify_string("ehhartbeat world hello 1. /livetv :- 1 jh dyuiyufds :jkhjkdsa sdahjkhas")
        expected = '0VUcFRAZ39T2WOIAb8DSHFY69BL32Nc15666EDO9A33GC1623'
        self.assertEquals(expected, actual)

        actual = unify_string("ehhartbeat world hello 1. /livetv -: 1 jh dyuiyufds :sdahjkhas jkhjkdsa")
        expected = '0VUcFRAZ39T2WOIAb8DSHFYA9aE50GMBc78NA2c'
        self.assertEquals(expected, actual)

        actual = unify_string("ehhartbeat world hello 1. /livetv -: 1 jh dyuiyufds :sdahjkhas jkhjkdsa jkhjkdsa jkhjkdsa jkhjkdsa jkhjkdsa jkhjkdsa jkhjkdsa")
        expected = 'VIYXY4Hb31939H3MW78P0bT8GPQ3P3135X5BX18770bAI0NZ95X4PP7bJ7C5W0UF1I3R8c36IQ5JU7Xc95LGKZYCbA6KR52'
        self.assertEquals(expected, actual)

        actual = unify_string("привітЖ 1.&jhорггг!")
        expected = 'G31PQb112WMS583R21H'
        self.assertEquals(expected, actual)


if __name__ == '__main__':
    unittest.main()
