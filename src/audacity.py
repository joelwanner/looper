import psutil
import time

from .pipeclient import PipeClient

TIMEOUT = 4


class AudacityConnector:
    def __init__(self, gain_db: float, bit_depth: int):
        self.gain_db = gain_db
        self.bit_depth = bit_depth

        # Check if Audacity is running
        if 'audacity' not in [p.name().lower() for p in psutil.process_iter()]:
            raise RuntimeError("Audacity is not running. Please start it")

        self.client = PipeClient()

    def _run(self, cmd: str) -> str:
        self.client.write(cmd)
        start = time.time()
        while time.time() < start + TIMEOUT:
            time.sleep(0.1)
            if reply := self.client.read():
                return reply
        raise TimeoutError

    def convert(self, in_path, out_path):
        def do(cmd, **kwargs):
            print(self._run(f"{cmd}: {', '.join(f'{k}={v}' for k, v in kwargs.items())}"))
        do("Help", Command="Open")
        return
        do("SelectAll")
        do("Normalize", PeakLevel=self.gain_db)
