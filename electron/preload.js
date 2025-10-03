const {contextBridge, ipcRenderer} = require('electron');

// Exposer les API de manière sécurisée au renderer
contextBridge.exposeInMainWorld('electronAPI', {
    // Sélection de fichiers
    selectXML: () => ipcRenderer.invoke('select-xml'),
    selectExcel: () => ipcRenderer.invoke('select-excel'),
    selectVideos: () => ipcRenderer.invoke('select-videos'),
    selectOutput: () => ipcRenderer.invoke('select-output'),

    // Traitement vidéo
    processVideo: (config) => ipcRenderer.invoke('process-video', config),

    // Écouter les événements de progression
    onProgress: (callback) => {
        ipcRenderer.on('processing-progress', (event, message) => callback(message));
    },
    onPercent: (callback) => {
        ipcRenderer.on('processing-percent', (event, percent) => callback(percent));
    },
    onError: (callback) => {
        ipcRenderer.on('processing-error', (event, error) => callback(error));
    },

    // Mises à jour
    checkUpdates: () => ipcRenderer.invoke('check-updates'),

    // Version de l'app
    getVersion: () => '1.0.0-alpha'
});
