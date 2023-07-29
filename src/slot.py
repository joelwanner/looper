from pathlib import Path
import re
import uuid
from shutil import copyfile
import xml.etree.ElementTree as ET


class Slot:
    def __init__(self, base_path: Path, idx: int) -> None:
        self.idx = idx
        self.path = base_path / f"Patch{str(idx).zfill(2)}"

    def exists(self) -> bool:
        return self.path.exists()

    def write_patch_xml(self, name: str) -> None:
        root = ET.Element('JamManPatch',
            xmlns="http://schemas.digitech.com/JamMan/Patch",
            device='JamManStereo',
            version='1',
        )
        slot_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, f"{self.idx}.loop")

        ET.SubElement(root, 'PatchName').text = name
        ET.SubElement(root, 'RhythmType').text = 'StudioKickAndHighHat'
        ET.SubElement(root, 'StopMode').text = 'StopInstantly'
        ET.SubElement(root, 'SettingsVersion').text = '1'
        ET.SubElement(root, 'ID').text = str(slot_uuid)
        ET.SubElement(root, 'Metadata')

        tree = ET.ElementTree(root)
        ET.indent(tree, ' '*4)
        tree.write(self.path / 'patch.xml', encoding='UTF-8', xml_declaration=True)

    def write_phrase_xml(self, path: Path, bpm: int, timesig: int) -> None:
        root = ET.Element('JamManPhrase',
            xmlns="http://schemas.digitech.com/JamMan/Phrase",
            version='1',
        )
        phrase_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, f"a.{self.idx}.loop")

        ET.SubElement(root, "BeatsPerMinute").text = str(bpm)
        ET.SubElement(root, "BeatsPerMeasure").text = str(timesig)
        ET.SubElement(root, "BpmValidated").text = '0'
        ET.SubElement(root, "IsLoop").text = '1'
        ET.SubElement(root, "IsReversed").text = '0'
        ET.SubElement(root, 'SettingsVersion').text = '1'
        ET.SubElement(root, 'AudioVersion').text = '1'
        ET.SubElement(root, 'ID').text = str(phrase_uuid)
        ET.SubElement(root, 'Metadata')

        tree = ET.ElementTree(root)
        ET.indent(tree, ' '*4)
        tree.write(path / 'phrase.xml', encoding='UTF-8', xml_declaration=True)

    def store(self, loop: Path) -> None:
        # Extract metadata
        if match := re.search(r'(\d+)\s*bpm', loop.stem):
            bpm = int(match.group(1))
        else:
            bpm = 120

        # Set up structure
        self.path.mkdir(exist_ok=True)
        phrase = self.path / 'PhraseA'
        phrase.mkdir(exist_ok=True)

        self.write_patch_xml(loop.name)
        self.write_phrase_xml(phrase, bpm, 4)
        filename = 'phrase' + loop.suffix
        copyfile(loop, phrase / filename)
