const { app, BrowserWindow, ipcMain, nativeImage } = require('electron');
const path = require('path');
const WinState = require('electron-win-state').default;

const createWindow = () => {
  const winState = new WinState({
    defaultWidth: 1000,
    defaultHeight: 800,
  });
  const win = new BrowserWindow({
    ...winState.winOptions,
    webPreferences: {
      preload: path.resolve(__dirname, './preload/index.js')
    },
    show: false,
    frame: false,
  });

  win.setMenu(null);
  win.loadURL('http://localhost:7000');
  win.webContents.openDevTools({
    mode: 'undocked',
    additionalFeatures: {
      'autofill': false
    }
  });
  winState.manage(win);
  win.setPosition(100, 100);

  win.on('ready-to-show', () => {
    win.show();
  });

  win.webContents.on('did-fail-load', (event, errorCode, errorDescription, validatedURL) => {
    console.error(`Failed to load URL: ${validatedURL}, Error: ${errorDescription}`);
  });

  win.webContents.on('did-finish-load', () => {
    win.webContents.send('window-object', {
      type: 'window-object',
      windowId: win.id
    });
  });

  ipcMain.on('move-window', (event, { windowId, x, y, width, height }) => {
    const win = BrowserWindow.fromId(windowId);
    if (win) {
      let newBounds = {
        x: parseInt(x),
        y: parseInt(y),
        width: parseInt(width),
        height: parseInt(height),
      }
      win.setBounds(newBounds);
    }
  });
};

app.whenReady().then(() => {
  createWindow();

  app.on('active', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

// 监听来自渲染进程的窗口操作请求
ipcMain.on('perform-window-action', (event, { windowId, action }) => {
  const win = BrowserWindow.fromId(windowId);
  if (win) {
    switch (action) {
      case 'close':
        win.close();
        break;
      case 'minimize':
        win.minimize();
        break;
      case 'maximize':
        if (win.isMaximized()) {
          win.unmaximize();
        } else {
          win.maximize();
        }
        break;
    }
  }
});