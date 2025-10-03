const {app, BrowserWindow, ipcMain, dialog} = require('electron');
const path = require('path');
const {spawn} = require('child_process');

let mainWindow;
let pythonProcess = null;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js')
        },
        autoHideMenuBar: true,
        icon: path.join(__dirname, '../build/icon.png')
    });

    mainWindow.loadFile('renderer/index.html');

    // DevTools en mode développement
    if (process.env.NODE_ENV === 'development') {
        mainWindow.webContents.openDevTools();
    }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (pythonProcess) {
        pythonProcess.kill();
    }
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// IPC Handlers

// Sélection de fichier XML
ipcMain.handle('select-xml', async () => {
    const result = await dialog.showOpenDialog(mainWindow, {
        properties: ['openFile'],
        filters: [{name: 'XML Files', extensions: ['xml']}]
    });
    return result.canceled ? null : result.filePaths[0];
});

// Sélection de fichier Excel
ipcMain.handle('select-excel', async () => {
    const result = await dialog.showOpenDialog(mainWindow, {
        properties: ['openFile'],
        filters: [{name: 'Excel Files', extensions: ['xlsx', 'xls']}]
    });
    return result.canceled ? null : result.filePaths[0];
});

// Sélection de vidéos
ipcMain.handle('select-videos', async () => {
    const result = await dialog.showOpenDialog(mainWindow, {
        properties: ['openFile', 'multiSelections'],
        filters: [{name: 'Video Files', extensions: ['mp4', 'mov', 'MP4', 'MOV']}]
    });
    return result.canceled ? [] : result.filePaths;
});

// Sélection du fichier de sortie
ipcMain.handle('select-output', async () => {
    const result = await dialog.showSaveDialog(mainWindow, {
        defaultPath: 'output_final.mp4',
        filters: [{name: 'Video Files', extensions: ['mp4']}]
    });
    return result.canceled ? null : result.filePath;
});

// Lancer le traitement vidéo
ipcMain.handle('process-video', async (event, {xmlPath, excelPath, videoFolder, outputPath}) => {
    return new Promise((resolve, reject) => {
        // Construire la commande Python
        const pythonScript = path.join(__dirname, '../main.py');

        // Lancer le processus Python
        pythonProcess = spawn('python', [
            pythonScript,
            '--xml', xmlPath,
            '--excel', excelPath,
            '--videos', videoFolder,
            '--output', outputPath
        ]);

        let outputData = '';
        let errorData = '';

        // Capturer stdout pour la progression
        pythonProcess.stdout.on('data', (data) => {
            const message = data.toString();
            outputData += message;

            // Envoyer la progression au renderer
            mainWindow.webContents.send('processing-progress', message);

            // Parser pour extraire le pourcentage si disponible
            const progressMatch = message.match(/(\d+)\/(\d+)/);
            if (progressMatch) {
                const current = parseInt(progressMatch[1]);
                const total = parseInt(progressMatch[2]);
                const percent = Math.round((current / total) * 100);
                mainWindow.webContents.send('processing-percent', percent);
            }
        });

        pythonProcess.stderr.on('data', (data) => {
            errorData += data.toString();
            mainWindow.webContents.send('processing-error', data.toString());
        });

        pythonProcess.on('close', (code) => {
            pythonProcess = null;

            if (code === 0) {
                resolve({success: true, message: 'Vidéo générée avec succès!'});
            } else {
                reject({success: false, message: `Erreur: ${errorData}`});
            }
        });

        pythonProcess.on('error', (err) => {
            pythonProcess = null;
            reject({success: false, message: `Erreur de lancement: ${err.message}`});
        });
    });
});

// Vérifier les mises à jour
ipcMain.handle('check-updates', async () => {
    const https = require('https');
    const currentVersion = app.getVersion();
    const repo = 'Pierre-AdrienLefevre/auto-padel-tennis-overlay';

    return new Promise((resolve) => {
        https.get(`https://api.github.com/repos/${repo}/releases/latest`, {
            headers: {'User-Agent': 'Padel-Overlay-App'}
        }, (res) => {
            let data = '';

            res.on('data', (chunk) => {
                data += chunk;
            });

            res.on('end', () => {
                try {
                    const release = JSON.parse(data);
                    const latestVersion = release.tag_name.replace('v', '');

                    if (latestVersion > currentVersion) {
                        resolve({
                            updateAvailable: true,
                            version: latestVersion,
                            url: release.html_url
                        });
                    } else {
                        resolve({updateAvailable: false});
                    }
                } catch (e) {
                    resolve({updateAvailable: false, error: e.message});
                }
            });
        }).on('error', (e) => {
            resolve({updateAvailable: false, error: e.message});
        });
    });
});
