#!/usr/bin/env python3
import os
import argparse
from pypdf import PdfWriter

def merge_pdfs(output_name, files_to_merge):
    writer = PdfWriter()
    
    for file in files_to_merge:
        if os.path.exists(file):
            print(f"Adding: {file}")
            writer.append(file)
        else:
            print(f"Warning: File not found - {file}")

    with open(output_name, "wb") as output_file:
        writer.write(output_file)
    print(f"\nSuccessfully created: {output_name}")

def main():
    parser = argparse.ArgumentParser(description="Zusammenführen von Bewerbungsunterlagen (PDF).")
    
    parser.add_argument("--mode", choices=["letter_misc", "full_misc", "cv_misc"], required=True,
                        help="letter_misc: Anschreiben + /misc | full_misc: Anschreiben + CV + /misc | cv_misc: CV + /misc")
    
    parser.add_argument("--output", default="Bewerbung.pdf",
                        help="Name der Ausgabedatei (Default: Bewerbung.pdf)")

    args = parser.parse_args()

    # Pfade definieren
    cv_path = "cv/document.pdf"
    letter_path = "letter/document.pdf"
    misc_dir = "misc"
    
    files_to_merge = []
    
    # Basis-Dokumente festlegen
    if args.mode == "letter_misc":
        files_to_merge = [letter_path]
    elif args.mode == "full_misc":
        files_to_merge = [letter_path, cv_path]
    elif args.mode == "cv_misc":
        files_to_merge = [cv_path]

    # Anhänge aus /misc hinzufügen (immer am Ende, alphabetisch sortiert)
    if os.path.exists(misc_dir):
        misc_files = sorted([os.path.join(misc_dir, f) for f in os.listdir(misc_dir) if f.lower().endswith(".pdf")])
        files_to_merge.extend(misc_files)
    else:
        print(f"Info: Verzeichnis '{misc_dir}' nicht gefunden oder leer. Es werden nur die Basis-Dokumente gemischt.")

    merge_pdfs(args.output, files_to_merge)

if __name__ == "__main__":
    main()
