from pathlib import Path

base = Path("winlator/app")

gradle = base / "build.gradle"
s = gradle.read_text()

old = "applicationId 'com.winlator'"
new = "applicationId 'com.winlator.diag'"

assert old in s, "Application ID not found"
gradle.write_text(s.replace(old, new, 1))

manifest = base / "src/main/AndroidManifest.xml"
s = manifest.read_text()

old = 'android:authorities="com.winlator.FileProvider"'
new = 'android:authorities="com.winlator.diag.FileProvider"'

assert old in s, "Manifest FileProvider not found"
manifest.write_text(s.replace(old, new, 1))

utils = base / "src/main/java/com/winlator/core/FileUtils.java"
s = utils.read_text()

old = '"com.winlator.FileProvider"'
new = '"com.winlator.diag.FileProvider"'

assert old in s, "Java FileProvider not found"
utils.write_text(s.replace(old, new, 1))

print("OK: Diagnostic application ID configured")
print("OK: FileProvider references updated")
