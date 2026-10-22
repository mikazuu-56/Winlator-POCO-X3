from pathlib import Path

base = Path("winlator/app/src/main/java/com/winlator")

guest = base / "xenvironment/components/GuestProgramLauncherComponent.java"
s = guest.read_text()

old = '''return ProcessHelper.exec(command, envVars, rootDir, (status) -> {
            synchronized (lock) {
                pid = -1;
            }
            if (terminationCallback != null) terminationCallback.call(status);
        });'''

new = '''final java.io.File logFile = new java.io.File(
            environment.getContext().getFilesDir(),
            "winlator-startup.log"
        );

        writeDiagnostic(logFile, "START");

        int result = ProcessHelper.exec(command, envVars, rootDir, (status) -> {
            writeDiagnostic(logFile, "EXIT STATUS: " + status);
            synchronized (lock) {
                pid = -1;
            }
            if (terminationCallback != null) terminationCallback.call(status);
        });

        if (result == -1) {
            writeDiagnostic(logFile, "LAUNCH FAILED");
        }

        return result;'''

if old not in s:
    raise SystemExit("ERROR: Guest launcher target not found")

s = s.replace(old, new, 1)

method = '''
    private static void writeDiagnostic(java.io.File file, String message) {
        try (java.io.FileWriter writer = new java.io.FileWriter(file, true)) {
            writer.write(System.currentTimeMillis() + " " + message + "\\n");
        } catch (Exception e) {
            android.util.Log.e("WINLATOR_DIAG", "Log write failed", e);
        }
    }

'''

marker = "    private int execGuestProgram() {"

if marker not in s:
    raise SystemExit("ERROR: Method insertion point not found")

s = s.replace(marker, method + marker, 1)
guest.write_text(s)

print("OK: Private diagnostic logging added")
