# Strict LaTeX Injection & Escaping Rules

**1. Special Character Escaping**
You must escape the following LaTeX reserved characters if they appear in the JSON text:
- Ampersand: `&` becomes `\&` (e.g., "R&D" -> "R\&D")
- Percent: `%` becomes `\%` (e.g., "100%" -> "100\%")
- Dollar: `$` becomes `\$`
- Hash: `#` becomes `\#` (e.g., "C#" -> "C\#")
- Underscore: `_` becomes `\_`

**2. German Typography & Umlauts**
- Assume the document uses `\usepackage[utf8]{inputenc}`. You may inject native German characters (ä, ö, ü, ß, Ä, Ö, Ü) directly. Do NOT use legacy escaping like `\"a` unless the document preamble explicitly lacks utf8 support.
- Dashes: Use an en-dash (`--`) for number ranges (e.g., "2020--2023", "10--15\%"). Use a standard hyphen (`-`) for compound words (e.g., "IT-Infrastruktur").
- Quotation Marks: If quotes are needed, use German typographic quotes `\glqq` (lower, left) and `\grqq` (upper, right) or standard standard straight quotes depending on the document's `csquotes` setup.

**3. Structural Integrity (The Golden Rule)**
- NEVER alter the document preamble (anything before `\begin{document}`).
- NEVER change the structural commands defined by the template (e.g., `\cventry`, `\cvitem`, `\makelettertitle`).
- ONLY replace the textual arguments inside the brackets `{}` or environments of the user's existing data. If a JSON array has fewer bullet points than the existing LaTeX file, delete the extra `\item` rows cleanly. If it has more, replicate the exact `\item` syntax.