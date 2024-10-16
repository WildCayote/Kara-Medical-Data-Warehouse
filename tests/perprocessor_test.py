import unittest
from scripts.data_cleaner import Preprocessor

class TestPreprocessor(unittest.TestCase):
    """
    Unit tests for the Preprocessor class.
    """

    def test_remove_emojis(self):
        text_with_emojis = "Hello 😊! How are you? 🚀"
        expected_output = "Hello ! How are you? "
        self.assertEqual(Preprocessor.remove_emojis(text_with_emojis), expected_output)

    def test_remove_special_characters(self):
        text_with_special_chars = "Hello! How are you? ፤ ። ፣"
        expected_output = "Hello How are you   "
        self.assertEqual(Preprocessor.remove_special_characters(text_with_special_chars), expected_output)

    def test_normalize_data(self):
        text_to_normalize = "ሃኅኃ ሑኁዅ ዓኣዐ"
        expected_output = "ሀሀሀ ሁሁሁ አአአ"
        self.assertEqual(Preprocessor.normalize_data(text_to_normalize), expected_output)

    def test_remove_extra_space(self):
        text_with_extra_space = "Hello     World!    \nThis is a test."
        expected_output = "Hello World! This is a test."
        self.assertEqual(Preprocessor.remove_extra_space(text_with_extra_space), expected_output)

    def test_preprocess_text(self):
        text_to_process = "Hello 😊! How are you? ፤ ። ፣ ሃኅኃ ሑኁዅ ዓኣዐ"
        expected_output = "Hello How are you ሀሀሀ ሁሁሁ አአአ"
        self.assertEqual(Preprocessor.preprocess_text(text_to_process), expected_output)

if __name__ == '__main__':
    unittest.main()