const { app,BrowserWindow} = require('electron') 
const path=require('path')
const WinState=require('electron-win-state').default

const createWindow=()=>{
  const winState=new WinState({
    defaultWidth:1000,
    defaultHeight:800
  })
  const win=new BrowserWindow({
    ...winState.winOptions,
    webPreferences:{
      preload:path.resolve(__dirname, './preload/index.js')
    },
    show:false
  })

  win.loadURL('http://localhost:7000')
  //打开控制台的语句
  win.webContents.openDevTools()

  winState.manage(win)

  win.on('ready-to-show',()=>{
    win.show()
  })
}

app.whenReady().then(()=>{
  createWindow()

  //MAC端兼容
  app.on('active',()=>{
    if(BrowserWindow.getAllWindows().length===0)createWindow()
  })
})
 //Windows端兼容
app.on('window-all-closed',()=>{
  if(process.platform!== 'darwin')app.quit()
})