from pathlib import Path

p = Path("winlator/app/src/main/java/com/winlator/core/ProcessHelper.java")
s = p.read_text()

# Simpan lokasi log yang diberikan oleh GuestProgramLauncherComponent.
marker = "    public static int exec(String command) {"
assert marker in s, "ERROR: exec marker not found"

addition = '''
    public static File diagnosticLogFile;

    private static void writeProcessDiagnostic(String message) {
        if (diagnosticLogFile == null) return;

        try (java.io.FileWriter writer =
                 new java.io.FileWriter(diagnosticLogFile, true)) {
            writer.write(System.currentTimeMillis() + " " + message + "\\n");
        }
        catch (Exception ignored) {}
    }

'''

s = s.replace(marker, addition + marker, 1)

# Catat tahap peluncuran.
old = '            java.lang.Process process = processBuilder.start();'
new = '''            writeProcessDiagnostic("PROCESS START ATTEMPT");
            java.lang.Process process = processBuilder.start();
            writeProcessDiagnostic("PROCESS START SUCCESS");'''

assert old in s, "ERROR: ProcessBuilder marker not found"
s = s.replace(old, new, 1)

# Catat apakah refleksi PID berhasil.
old = '            pid = pidField.getInt(process);'
new = '''            pid = pidField.getInt(process);
            writeProcessDiagnostic("PID SUCCESS: " + pid);'''

assert old in s, "ERROR: PID marker not found"
s = s.replace(old, new, 1)

# Jangan lagi membuang exception.
old = '''        catch (Exception e) {}
        return pid;'''

new = '''        catch (Exception e) {
            writeProcessDiagnostic(
                "PROCESS EXCEPTION: " +
                android.util.Log.getStackTraceString(e)
            );
        }
        return pid;'''

assert old in s, "ERROR: Exception marker not found"
s = s.replace(old, new, 1)

p.write_text(s)

# Hubungkan lokasi log dengan GuestProgramLauncherComponent.
guest = Path(
    "winlator/app/src/main/java/com/winlator/"
    "xenvironment/components/GuestProgramLauncherComponent.java"
)

g = guest.read_text()

marker = '        writeDiagnostic(logFile, "START");'

assert marker in g, "ERROR: Guest log marker not found"

g = g.replace(
    marker,
    marker + "\n" +
    "        ProcessHelper.diagnosticLogFile = logFile;",
    1
)

guest.write_text(g)

print("OK: ProcessHelper exception logging")
print("OK: ProcessBuilder stage logging")
print("OK: PID reflection logging")
print("OK: Guest launcher log connection")
