from pathlib import Path
import json
import subprocess
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugin"


class TestDayBlocksPackage(unittest.TestCase):
    def test_manifest_identity(self):
        m = json.loads((PLUGIN / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(m["id"], "sp-day-blocks")
        self.assertEqual(m["name"], "Day Blocks")
        self.assertEqual(m["version"], "0.1.1-beta.1")
        self.assertTrue(m["iFrame"])
        for permission in ("getTasks", "getAllSimpleCounters", "loadSyncedData", "persistDataSynced", "updateTask", "setCounter"):
            self.assertIn(permission, m["permissions"])

    def test_bundle_has_exact_root_files(self):
        subprocess.run(["python", str(ROOT / "scripts/package.py")], check=True)
        with zipfile.ZipFile(ROOT / "dist/day-blocks-super-productivity.zip") as z:
            self.assertEqual(z.namelist(), ["manifest.json", "plugin.js", "index.html", "icon.svg"])
            self.assertIsNone(z.testzip())
            self.assertEqual(json.loads(z.read("manifest.json"))["version"], "0.1.1-beta.1")

    def test_standalone_identity(self):
        js = (PLUGIN / "plugin.js").read_text(encoding="utf-8")
        html = (PLUGIN / "index.html").read_text(encoding="utf-8")
        self.assertIn("Day Blocks", js)
        self.assertIn("Day Blocks", html)
        self.assertNotIn("sp-today-tasks-habits", js + html)
        self.assertIn("day-blocks.plans.v1", html)
        self.assertIn("repeat(4,minmax(", html)
        self.assertIn("grid-auto-flow:column", html)

    def test_javascript_syntax(self):
        html = (PLUGIN / "index.html").read_text(encoding="utf-8")
        script = html.split("<script>", 1)[1].split("</script>", 1)[0]
        for source in (script, (PLUGIN / "plugin.js").read_text(encoding="utf-8")):
            result = subprocess.run(["node", "--check"], input=source, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_planner_contract(self):
        html = (PLUGIN / "index.html").read_text(encoding="utf-8")
        for symbol in ("function visibleSessions()", "function moveSession(",
                       "function addFlexible(", "function saveSession(",
                       "function removeSession(", "function habitDue(",
                       "function saveHabitLog(", "function render()",
                       "function normalizeData(", "persistDataSynced(data,STORAGE)"):
            self.assertIn(symbol, html)
        self.assertIn("background:transparent!important", html)
        self.assertIn("data-drop-block", html)
        self.assertIn("data-copy-session", html)


if __name__ == "__main__":
    unittest.main()
