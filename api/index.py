import sys
import os
import tempfile

# Ensure safe serverless temporary directory
if os.name != 'nt':
    os.environ.setdefault('TMPDIR', '/tmp')
    os.environ.setdefault('TEMP', '/tmp')
    os.environ.setdefault('TMP', '/tmp')
    try:
        tempfile.tempdir = '/tmp'
    except Exception:
        pass

# Add root directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot import app

# Export WSGI application for Vercel Serverless
app = app
