import unittest
from contacts_manager import validate_phone, validate_email


class TestContactValidation(unittest.TestCase):

    def test_valid_phone(self):
        self.assertTrue(validate_phone("123-456-7890")[0])

    def test_invalid_phone(self):
        self.assertFalse(validate_phone("123")[0])

    def test_valid_email(self):
        self.assertTrue(validate_email("test@email.com"))

    def test_invalid_email(self):
        self.assertFalse(validate_email("invalid-email"))


if __name__ == "__main__":
    unittest.main()