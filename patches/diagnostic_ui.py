from pathlib import Path

p = Path("winlator/app/src/main/java/com/winlator/MainActivity.java")
s = p.read_text()

marker = "        setSupportActionBar(findViewById(R.id.Toolbar));"
assert marker in s, "Toolbar marker not found"

addition = '''
        android.view.View toolbarView = findViewById(R.id.Toolbar);

        if (toolbarView instanceof android.view.ViewGroup) {
            android.widget.Button logButton =
                new android.widget.Button(this);

            logButton.setText("LOG");
            logButton.setTextSize(12);

            ((android.view.ViewGroup) toolbarView).addView(
                logButton,
                new android.view.ViewGroup.LayoutParams(
                    android.view.ViewGroup.LayoutParams.WRAP_CONTENT,
                    android.view.ViewGroup.LayoutParams.MATCH_PARENT
                )
            );

            logButton.setOnClickListener(v -> showDiagnosticLog());
        }

'''

s = s.replace(marker, marker + "\n" + addition, 1)

marker2 = "    @Override\n    protected void attachBaseContext("

assert marker2 in s, "Method insertion marker not found"

method = '''
    private void showDiagnosticLog() {
        java.io.File file = new java.io.File(
            getFilesDir(),
            "winlator-startup.log"
        );

        String content;

        try {
            if (!file.exists()) {
                content = "Belum ada log. Jalankan container dahulu.";
            }
            else {
                byte[] bytes = java.nio.file.Files.readAllBytes(
                    file.toPath()
                );

                content = new String(
                    bytes,
                    java.nio.charset.StandardCharsets.UTF_8
                );
            }
        }
        catch (Exception e) {
            content = "Gagal membaca log: " + e;
        }

        final String result = content;

        new android.app.AlertDialog.Builder(this)
            .setTitle("Winlator Startup Log")
            .setMessage(result)
            .setPositiveButton("Salin Log", (dialog, which) -> {
                android.content.ClipboardManager clipboard =
                    (android.content.ClipboardManager)
                    getSystemService(CLIPBOARD_SERVICE);

                clipboard.setPrimaryClip(
                    android.content.ClipData.newPlainText(
                        "Winlator Log",
                        result
                    )
                );

                android.widget.Toast.makeText(
                    this,
                    "Log disalin",
                    android.widget.Toast.LENGTH_SHORT
                ).show();
            })
            .setNegativeButton("Tutup", null)
            .show();
    }

'''

s = s.replace(marker2, method + marker2, 1)

p.write_text(s)

print("OK: LOG button added")
print("OK: Copy log dialog added")
