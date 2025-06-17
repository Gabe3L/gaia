import { app, BrowserWindow, Menu } from 'electron';
import { spawn } from 'child_process';
import * as path from 'path';
import * as http from 'http';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let mainWindow = null;
let backendProcess = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  mainWindow.webContents.session.clearCache().then(() => { // TODO: Remove for prod
    if (mainWindow) mainWindow.loadURL("http://127.0.0.1:8000");
  });

  mainWindow.webContents.openDevTools(); // TODO: Remove for prod
  mainWindow.maximize();

  Menu.setApplicationMenu(null);
}

function startBackend() {
  const scriptPath = path.resolve(__dirname, 'backend', 'start.py');

  backendProcess = spawn('python', [scriptPath]);

  if (backendProcess.stdout) {
    backendProcess.stdout.on('data', (data) => {
      console.log(`[Backend]: ${data}`);
    });
  }

  if (backendProcess.stderr) {
    backendProcess.stderr.on('data', (data) => {
      console.log(`[Backend]: ${data}`);
    });
  }

  backendProcess.on('close', (code) => {
    console.log(`[Backend] Exited with code ${code}`);
  });
}

function waitForBackendReady() {
  let dotCount = 1;

  const tryConnect = () => {
    http.get('http://127.0.0.1:8000/', () => {
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
