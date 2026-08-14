import os
from bot import app, bot, TOKEN

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5005))
    print(f"ATLAS Platformasi ishga tushdi: http://localhost:{port}/")
    app.run(host="0.0.0.0", port=port, debug=False)

