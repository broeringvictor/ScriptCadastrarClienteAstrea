# Disable the __del__ method to prevent automatic cleanup
self.driver.__del__ = lambda *_: None