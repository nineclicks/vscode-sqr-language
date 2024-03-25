const vscode = require('vscode');
const CustomSymbolProvider = require('./symbolProvider');

function activate(context) {
  let provider = new CustomSymbolProvider();
  let disposable = vscode.languages.registerDocumentSymbolProvider({ language: 'sqr' }, provider);

  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate
};

console.log(`SQR extension main`);