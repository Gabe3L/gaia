const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const http = require('http');

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

  mainWindow.loadURL('http://localhost:8000');
}

function startBackend() {
  const scriptPath = path.resolve(__dirname, '..', 'backend', 'start.py');
  
  backendProcess = spawn('python', [scriptPath]);
  
  backendProcess.stdout.on('data', (data) => {
    console.log(`[Backend]: ${data}`);
  });

  backendProcess.stderr.on('data', (data) => {
    console.error(`[Backend Error]: ${data}`);
  });

  backendProcess.on('close', (code) => {
    console.log(`Backend exited with code ${code}`);
  });
}

function waitForBackendReady(retries = 20) {
  const tryConnect = () => {
    http.get('http://localhost:8000', () => {
      console.log('Backend is ready');
      createWindow();
    }).on('error', () => {
      if (retries > 0) {
        console.log('Waiting for backend...');
        setTimeout(() => waitForBackendReady(retries - 1), 1000);
      } else {
        console.error('Backend failed to start');
      }
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
