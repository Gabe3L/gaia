const { app, BrowserWindow, Menu } = require('electron');
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

  mainWindow.webContents.session.clearCache().then(() => { // TODO: Remove for prod
    mainWindow.loadURL('http://localhost:8000');
  });

  mainWindow.maximize(true);
  
  Menu.setApplicationMenu(null);
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

function waitForBackendReady() {
  let dotCount = 1;

  const tryConnect = () => {
    http.get('http://localhost:8000', () => {
      console.log('Backend is ready');
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
