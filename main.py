""" Linkifies the card names in a Star Realms log. """
import re
import subprocess
import sys
from pathlib import Path

WIKI_PATH = "https://starrealms.fandom.com/wiki/{}"
if __name__ == '__main__':
    newlines = []
    highlight = False
    background_color = "#FFFFFF"
    with open("log.txt") as log:
        for line in log:
            pattern = r"<color=#(.{6})>(.*)</color>"
            repl = r'<a style="color: #\1; ext-decoration:underline;" href="https://starrealms.fandom.com/wiki/\2">\2</a>'
            new_line = re.sub(pattern, repl, line)

            new_line = re.sub("#FFFF00", "#CCCC00", new_line)
            match = re.search(r"It is now (.+)'s turn (.+)", new_line)
            if match:
                player = match.group(1)
                turn = match.group(2)
                highlight = not highlight
                background_color = "#EEEEEE" if highlight else "white"
            new_line = f"<span style='white-space:pre-wrap;background-color:{background_color}'>{new_line}</span>"

            # new_line = re.sub(r"^([ ]+", )
            newlines.append(new_line)
    html_template_path = Path("html_template.html")
    formatted_text = html_template_path.read_text().format(text="\n".join(newlines))
    outputfile = Path("log.html")
    outputfile.write_text(formatted_text)

    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, outputfile])

