import unittest

from urls_crowler.run_crowlers import run_crowlers_threading


class TestMainApp(unittest.IsolatedAsyncioTestCase):
    async def test_main_app(self):
        await run_crowlers_threading()
