// État de l'application
let appState = {
    xmlPath: '',
    excelPath: '',
    videoFolder: '',
    outputPath: 'output_final.mp4',
    isProcessing: false
};

// Éléments DOM
const elements = {
    xmlPath: document.getElementById('xml-path'),
    excelPath: document.getElementById('excel-path'),
    videoPath: document.getElementById('video-path'),
    outputPath: document.getElementById('output-path'),
    btnXml: document.getElementById('btn-xml'),
    btnExcel: document.getElementById('btn-excel'),
    btnVideos: document.getElementById('btn-videos'),
    btnOutput: document.getElementById('btn-output'),
    btnGenerate: document.getElementById('btn-generate'),
    progressContainer: document.getElementById('progress-container'),
    progressFill: document.getElementById('progress-fill'),
    progressText: document.getElementById('progress-text'),
    timeRemaining: document.getElementById('time-remaining'),
    logOutput: document.getElementById('log-output'),
    checkUpdates: document.getElementById('check-updates'),
    appVersion: document.getElementById('app-version')
};

// Initialisation
window.addEventListener('DOMContentLoaded', () => {
    // Afficher la version
    elements.appVersion.textContent = window.electronAPI.getVersion();

    // Event listeners pour les boutons de sélection
    elements.btnXml.addEventListener('click', selectXML);
    elements.btnExcel.addEventListener('click', selectExcel);
    elements.btnVideos.addEventListener('click', selectVideos);
    elements.btnOutput.addEventListener('click', selectOutput);
    elements.btnGenerate.addEventListener('click', generateVideo);
    elements.checkUpdates.addEventListener('click', checkUpdates);

    // Écouter les événements de progression
    window.electronAPI.onProgress((message) => {
        log(message);
    });

    window.electronAPI.onPercent((percent) => {
        updateProgress(percent);
    });

    window.electronAPI.onError((error) => {
        log(`ERROR: ${error}`, 'error');
    });

    log('Application prête!', 'success');
});

// Fonctions de sélection de fichiers
async function selectXML() {
    const path = await window.electronAPI.selectXML();
    if (path) {
        appState.xmlPath = path;
        elements.xmlPath.value = path;
        log(`✓ XML sélectionné: ${getFileName(path)}`);
    }
}

async function selectExcel() {
    const path = await window.electronAPI.selectExcel();
    if (path) {
        appState.excelPath = path;
        elements.excelPath.value = path;
        log(`✓ Excel sélectionné: ${getFileName(path)}`);
    }
}

async function selectVideos() {
    const paths = await window.electronAPI.selectVideos();
    if (paths && paths.length > 0) {
        // Utiliser le dossier du premier fichier
        appState.videoFolder = getDirName(paths[0]);
        const displayText = paths.length === 1
            ? paths[0]
            : `${paths.length} fichiers dans ${appState.videoFolder}`;
        elements.videoPath.value = displayText;

        log(`✓ ${paths.length} fichier(s) vidéo sélectionné(s)`);
        paths.slice(0, 3).forEach(p => log(`  • ${getFileName(p)}`));
        if (paths.length > 3) log(`  ... et ${paths.length - 3} autre(s)`);
    }
}

async function selectOutput() {
    const path = await window.electronAPI.selectOutput();
    if (path) {
        appState.outputPath = path;
        elements.outputPath.value = path;
        log(`✓ Sortie: ${getFileName(path)}`);
    }
}

// Fonction principale de génération
async function generateVideo() {
    // Debug: afficher l'état
    console.log('État de l\'application:', appState);

    // Validation
    if (!appState.xmlPath || !appState.excelPath || !appState.videoFolder) {
        console.error('Fichiers manquants:', {
            xml: !!appState.xmlPath,
            excel: !!appState.excelPath,
            videoFolder: !!appState.videoFolder
        });
        alert(`Veuillez sélectionner tous les fichiers requis!\n\nXML: ${appState.xmlPath ? '✓' : '✗'}\nExcel: ${appState.excelPath ? '✓' : '✗'}\nVidéos: ${appState.videoFolder ? '✓' : '✗'}`);
        return;
    }

    // Désactiver le bouton
    appState.isProcessing = true;
    elements.btnGenerate.disabled = true;
    elements.progressContainer.style.display = 'block';

    // Réinitialiser la progression
    updateProgress(0);
    elements.timeRemaining.textContent = 'Démarrage...';

    log('\n' + '='.repeat(50));
    log('DÉMARRAGE DU TRAITEMENT');
    log('='.repeat(50));

    try {
        // Lancer le traitement
        const result = await window.electronAPI.processVideo({
            xmlPath: appState.xmlPath,
            excelPath: appState.excelPath,
            videoFolder: appState.videoFolder,
            outputPath: appState.outputPath || 'output_final.mp4'
        });

        // Succès
        updateProgress(100);
        log('\n' + '='.repeat(50));
        log(result.message, 'success');
        log('='.repeat(50));

        alert('✅ Vidéo générée avec succès!');

    } catch (error) {
        // Erreur
        log('\n' + '='.repeat(50));
        log(`ERREUR: ${error.message}`, 'error');
        log('='.repeat(50));

        alert(`❌ Erreur lors de la génération:\n${error.message}`);
    } finally {
        // Réactiver le bouton
        appState.isProcessing = false;
        elements.btnGenerate.disabled = false;
        elements.progressContainer.style.display = 'none';
    }
}

// Mettre à jour la barre de progression
function updateProgress(percent) {
    elements.progressFill.style.width = `${percent}%`;
    elements.progressText.textContent = `${percent}%`;
}

// Ajouter un message au log
function log(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    const prefix = type === 'error' ? '❌' : type === 'success' ? '✅' : '•';
    const logLine = `[${timestamp}] ${prefix} ${message}\n`;

    elements.logOutput.textContent += logLine;

    // Auto-scroll
    elements.logOutput.scrollTop = elements.logOutput.scrollHeight;
}

// Vérifier les mises à jour
async function checkUpdates(e) {
    e.preventDefault();
    log('Vérification des mises à jour...');

    const result = await window.electronAPI.checkUpdates();

    if (result.updateAvailable) {
        const confirmed = confirm(
            `Une nouvelle version (${result.version}) est disponible!\n\n` +
            `Version actuelle: ${window.electronAPI.getVersion()}\n` +
            `Nouvelle version: ${result.version}\n\n` +
            `Voulez-vous télécharger la mise à jour?`
        );

        if (confirmed) {
            window.open(result.url, '_blank');
        }
    } else if (result.error) {
        log(`Impossible de vérifier les mises à jour: ${result.error}`, 'error');
    } else {
        log('Application à jour!', 'success');
        alert('✅ Vous utilisez la dernière version!');
    }
}

// Utilitaires
function getFileName(path) {
    return path.split(/[/\\]/).pop();
}

function getDirName(path) {
    // Trouver la dernière occurrence de / ou \
    const lastSlash = Math.max(path.lastIndexOf('/'), path.lastIndexOf('\\'));
    return lastSlash > 0 ? path.substring(0, lastSlash) : path;
}
