# Dokumentation for brug af AI
## CSS
Et problem med CSS, hvor mit mainwindow udstrækker sig ud fra viewporten. 
PROMPT: "jeg har et problem, hvori min mainwindow går uden for min viewport" *konteskt kode gives*
Løsningsforslag: erstat body margin med body padding  og tilføj box-sizing: border-box;
Erstat også min-width: 100%; med flex: 1; min-width: 0;
