import unittest


from cart.api.v1 import utility


class test_key(unittest.TestCase):

    def test_01(self):
        customer_id = 123
        expect = "v1_123"
        output = utility.key(customer_id)
        self.assertEqual(expect, output)


class test_manager(unittest.TestCase):
    pass


class test_limit(unittest.TestCase):

    def test_01(self):
        data = [0, 1, 2, 3, 4, 5]
        num = 3
        expect = [0, 1, 2]
        output = utility.limit(data, num)
        self.assertListEqual(expect, output)

    def test_02(self):
        data = [0, 1, 2, 3, 4, 5]
        num = -1
        expect = [0, 1, 2, 3, 4]
        output = utility.limit(data, num)
        self.assertListEqual(expect, output)

    def test_03(self):
        data = [0, 1, 2, 3, 4, 5]
        num = 10
        expect = [0, 1, 2, 3, 4, 5]
        output = utility.limit(data, num)
        self.assertListEqual(expect, output)

    def test_04(self):
        data = [0, 1, 2, 3, 4, 5]
        num = 6
        expect = [0, 1, 2, 3, 4, 5]
        output = utility.limit(data, num)
        self.assertListEqual(expect, output)

    def test_05(self):
        data = [0, 1, 2, 3, 4, 5]
        num = 0
        expect = []
        output = utility.limit(data, num)
        self.assertListEqual(expect, output)

    def test_06(self):
        data = []
        num = 20
        expect = []
        output = utility.limit(data, num)
        self.assertListEqual(expect, output)

    def test_bad_01(self):
        data = [0, 1, 2, 3, 4]
        num = "string"
        expect = [0, 1, 2, 3, 4]
        output = utility.limit(data, num)
        self.assertEqual(expect, output)

    def test_bad_02(self):
        data = [0, 1, 2, 3, 4]
        num = None
        expect = [0, 1, 2, 3, 4]
        output = utility.limit(data, num)
        self.assertEqual(expect, output)


class test_offset(unittest.TestCase):

    def test_01(self):
        data = [0, 1, 2, 3, 4, 5]
        num = 3
        expect = [3, 4, 5]
        output = utility.offset(data, num)
        self.assertListEqual(expect, output)

    def test_02(self):
        data = [0, 1, 2, 3, 4, 5]
        num = 0
        expect = [0, 1, 2, 3, 4, 5]
        output = utility.offset(data, num)
        self.assertListEqual(expect, output)

    def test_03(self):
        data = [0, 1, 2, 3, 4, 5]
        num = 20
        expect = []
        output = utility.offset(data, num)
        self.assertListEqual(expect, output)

    def test_04(self):
        data = [0, 1, 2, 3, 4, 5]
        num = -2
        expect = [4, 5]
        output = utility.offset(data, num)
        self.assertListEqual(expect, output)

    def test_05(self):
        data = []
        num = 20
        expect = []
        output = utility.offset(data, num)
        self.assertListEqual(expect, output)

    def test_bad_01(self):
        data = [1, 2, 3, 4]
        num = "string"
        expect = [1, 2, 3, 4]
        output = utility.offset(data, num)
        self.assertListEqual(expect, output)

    def test_bad_02(self):
        data = [1, 2, 3, 4]
        num = None
        expect = [1, 2, 3, 4]
        output = utility.offset(data, num)
        self.assertListEqual(expect, output)


class test_fields(unittest.TestCase):
    pass


class test_fieldsList(unittest.TestCase):

    def test_01(self):
        data = [
            {
                "cat": "meow",
                "dog": "bark"
            },
            {
                "fish": "bubbles"
            }
        ]
        keys = {"cat", "fish"}
        expect = [
            {
                "cat": "meow"
            },
            {
                "fish": "bubbles"
            }
        ]
        output = utility._fieldsList(data, keys)
        self.assertListEqual(expect, output)

    def test_02(self):
        data = [
            {
                "cat": "meow",
                "dog": "bark"
            },
            {
                "fish": "bubbles"
            }
        ]
        keys = {"cat"}
        expect = [
            {
                "cat": "meow"
            }
        ]
        output = utility._fieldsList(data, keys)
        self.assertListEqual(expect, output)


class test_fieldsDict(unittest.TestCase):

    def test_01(self):
        data = {
            "cat": "meow",
            "dog": "bark"
        }
        keys = {"cat"}
        expect = {"cat": "meow"}
        output = utility._fieldsDict(data, keys)
        self.assertDictEqual(expect, output)

    def test_02(self):
        data = {
            "cat": "meow",
            "dog": "bark"
        }
        keys = {"fish", "cat"}
        expect = {"cat": "meow"}
        output = utility._fieldsDict(data, keys)
        self.assertDictEqual(expect, output)


if __name__ == '__main__':
    unittest.main()
