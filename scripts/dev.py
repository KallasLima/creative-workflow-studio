from pathlib import Path
import os,sys,subprocess,signal,socket
ROOT=Path(__file__).resolve().parents[1]
BACKEND=ROOT/'project/poc/backend'
FRONTEND=ROOT/'project/poc/frontend'
PYTHON=ROOT/'.venv'/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
NODE='node'
children=[]
for port in (4531,4532):
    with socket.socket() as probe:
        try: probe.bind(('127.0.0.1',port))
        except OSError: raise SystemExit(f'Port {port} is occupied. Use a different local environment; do not stop unrelated services.')
if not PYTHON.exists(): raise SystemExit('Create .venv and install backend requirements first; see README.md.')
env=os.environ.copy();env['VITE_API_BASE_URL']='http://127.0.0.1:4531'
try:
    children.append(subprocess.Popen([str(PYTHON),'-m','uvicorn','app.main:app','--host','127.0.0.1','--port','4531'],cwd=BACKEND,env=env))
    children.append(subprocess.Popen([NODE,str(FRONTEND/'node_modules/vite/bin/vite.js')],cwd=FRONTEND,env=env))
    print('Open http://127.0.0.1:4532. The API persists to a local ignored SQLite file. Ctrl+C stops this launcher’s children.',flush=True)
    while all(child.poll() is None for child in children):
        try: children[0].wait(timeout=1)
        except subprocess.TimeoutExpired: pass
except KeyboardInterrupt: pass
finally:
    for child in children:
        if child.poll() is None: child.terminate()
    for child in children:
        try: child.wait(timeout=5)
        except subprocess.TimeoutExpired: child.kill();child.wait()
