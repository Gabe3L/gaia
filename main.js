import { app, BrowserWindow, Menu } from 'electron';
import { spawn } from 'child_process';
import path from 'path';
import http from 'http';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let mainWindow;
let backendProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  mainWindow.webContents.session.clearCache().then(() => { // TODO: Remove for prod
    mainWindow.loadFile(path.join(__dirname, 'build', 'index.html'));
  });

  mainWindow.webContents.openDevTools(); // TODO: Remove for prod
  mainWindow.maximize(true);

  Menu.setApplicationMenu(null);
}

function startBackend() {
  const scriptPath = path.resolve(__dirname, 'backend', 'start.py');

  backendProcess = spawn('python', [scriptPath]);

  backendProcess.stdout.on('data', (data) => {
    console.log(`[Backend]: ${data}`);
  });

  backendProcess.stderr.on('data', (data) => {
    console.log(`[Backend]: ${data}`);
  });

  backendProcess.on('close', (code) => {
    console.log(`[Backend] Exited with code ${code}`);
  });
}

function waitForBackendReady() {
  let dotCount = 1;

  const tryConnect = () => {
    http.get('http://127.0.0.1:8000/ready', () => {
      console.log('[Backend] INFO:     Backend is ready');
      createWindow();
    }).on('error', () => {
      process.stdout.write('Waiting for backend' + '.'.repeat(dotCount) + '   ');
      process.stdout.write('\r');

      dotCount = (dotCount % 3) + 1;

      setTimeout(tryConnect, 1000);
    });
  };
  tryConnect();
}

app.whenReady().then(() => {
  startBackend();
  waitForBackendReady();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('will-quit', () => {
  if (backendProcess) {
    backendProcess.kill();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
