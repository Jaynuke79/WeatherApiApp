import unittest
import WeatherWizard.weather.funcs as funcs


class TestFuncs(unittest.TestCase):

    def test_constants_types(self):
        self.assertIsInstance(funcs.BASE_URL, str)
        self.assertTrue(funcs.BASE_URL.startswith("http"))

        self.assertIsInstance(funcs.GEOCODE_URL, str)
        self.assertTrue(funcs.GEOCODE_URL.startswith("http"))

        self.assertIsInstance(funcs.LATITUDE, float)
        self.assertIsInstance(funcs.LONGITUDE, float)
    
    def test_console_is_rich_console(self):
        from rich.console import Console
        self.assertIsInstance(funcs.console, Console)
        funcs.console.print("test")  # Ensures the object is used

    def test_constants_types(self):
        self.assertIsInstance(funcs.BASE_URL, str)
        self.assertTrue(funcs.BASE_URL.startswith("http"))

        self.assertIsInstance(funcs.GEOCODE_URL, str)
        self.assertTrue(funcs.GEOCODE_URL.startswith("http"))

        self.assertIsInstance(funcs.LATITUDE, float)
        self.assertIsInstance(funcs.LONGITUDE, float)




if __name__ == "__main__":
    unittest.main()
