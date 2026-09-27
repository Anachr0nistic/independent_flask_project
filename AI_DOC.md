# Dokumentation for brug af AI
## CSS
Et problem med CSS, hvor mit mainwindow udstrækker sig ud fra viewporten. 
PROMPT: "jeg har et problem, hvori min mainwindow går uden for min viewport" *konteskt kode gives*
Løsningsforslag: height: calc(100vh-30px), hvor 30px er margin og 100vh er viewport højden.

## SIDEOPDATERING
Jeg ville gerne vise ny information på en side uden at lave en hel ny HTML template
prompt: "Jeg har en Home page, hvor jeg har en sidebjælke, hvor der er en knap til at upload videoer og så se videoer. Når jeg klikker på disse knapper ville jeg gerne have min main container til at opdatere indholdet uden at render en ny template"

løsningsforslag: HTMX og partials. Den forslog jeg laver partials, som er mindre html dokumenter, med kun de relevante dele (uden html, head og body tags). 
