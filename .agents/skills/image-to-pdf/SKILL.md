---
name: image-to-pdf
description: "Scans the workspace directory for common image formats (.png, .jpg, .jpeg) and packs them sequentially into a single target PDF."
---

# Image-to-PDF Agent Skill

This skill allows Google Antigravity to pack all image files from the workspace directory into a single PDF document.

## Triggers
This skill triggers automatically when the user:
- Asks to convert, compile, or pack images into a PDF.
- Runs the `/img2pdf` custom command.

## Instructions
1. Scan the current working directory for common image formats (`.png`, `.jpg`, `.jpeg`).
2. Sort them alphabetically or by custom configuration.
3. If no images are found, notify the user.
4. Execute the Python script at `scripts/image_to_pdf.py` using python to compile them.
5. Save the output PDF as requested by the user, defaulting to `images_combined.pdf`.
