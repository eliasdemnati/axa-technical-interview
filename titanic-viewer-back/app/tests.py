#!/usr/bin/env python3

import unittest


# Not implemented but idea of the structure

class GetPassengers(unittest.TestCase):
    def test_success(self):
        self.assertEqual(1, 1)

    def test_success_with_search_value(self):
        self.assertEqual(1, 1)


class GetPassenger(unittest.TestCase):
    def test_success(self):
        self.assertEqual(1, 1)

    def test_error_with_wrong_id(self):
        self.assertEqual(1, 1)


class PostPassenger(unittest.TestCase):
    def test_success(self):
        self.assertEqual(1, 1)

    def test_error_with_wrong_data(self):
        self.assertEqual(1, 1)


if __name__ == "__main__":
    unittest.main()
