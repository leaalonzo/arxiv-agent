from flask import Flask
from datetime import date

app = Flask(__name__)

@app.route("/")
def index():
    try:
        with open("/home/pi/arxiv-agent/digest.log") as f:
            content = f.read()
        lines = content.strip().split("\n")
        html_lines = ""
        for line in lines:
            if line.startswith("==="):
                html_lines += f"<h2>{line}</h2>"
            elif line.startswith("📄"):
                html_lines += f"<h3>{line}</h3>"
            elif line.startswith("   http"):
                html_lines += f"<a href='{line.strip()}' target='_blank'>{line.strip()}</a><br><br>"
            elif line.strip():
                html_lines += f"<p>{line}</p>"
    except:
        html_lines = "<p>No digest yet — wait for the 7am run or trigger manually.</p>"

    return f"""
    <html>
    <head>
        <title>ArXiv Digest</title>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; 
                   margin: 40px auto; padding: 0 20px; background: #f5f5f5; }}
            h2 {{ color: #333; border-bottom: 2px solid #00c896; padding-bottom: 8px; }}
            h3 {{ color: #222; margin-bottom: 4px; }}
            p {{ color: #555; line-height: 1.6; }}
            a {{ color: #00c896; }}
        </style>
    </head>
    <body>
        {html_lines}
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
