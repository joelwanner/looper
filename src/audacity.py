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
        self._setup()

    def _run(self, cmd: str, **kwargs) -> str:
        full_cmd = f"{cmd}: {', '.join(f'{k}={v}' for k, v in kwargs.items())}" if kwargs else cmd
        self.client.write(full_cmd)
        start = time.time()
        while time.time() < start + TIMEOUT:
            time.sleep(0.1)
            if reply := self.client.read():
                return reply
        raise TimeoutError

    def _setup(self) -> None:
        self._run("SetProject")

    def _cleanup(self) -> None:
        self._run("Select", TrackCount=2)
        self._run("RemoveTracks")

    def convert(self, in_path, out_path):
        self._cleanup()
        self._run("Import2", Filename=in_path)
        self._run("SelectAll")
        self._run("Normalize", PeakLevel=self.gain_db)
        self._run("ExportWav", Filename=out_path)
