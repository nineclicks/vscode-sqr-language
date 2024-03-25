const vscode = require('vscode');

class CustomSymbolProvider {
  provideDocumentSymbols(document, token) {

    try {
      return [
        ...getFunctionNames(document),
        //...getVariableNames(document), // This is not great or helpful yet
      ]

    } catch (ex) {
      console.log(ex)
    }

  }
}

function getVariableNames(document) {
  const varReg = /([$#&](?!(debug|define|else|end-if|include|if|ifdef|ifndef)[^\w-])[\w-]+)(?=[^\w-])/gi
  const text = document.getText();
  const matches = [...text.matchAll(varReg)];

  return matches.map(match => {
    const start = match.index;
    const end = start + match[0].length;
    let range = new vscode.Range(document.positionAt(start), document.positionAt(end));
    return new vscode.DocumentSymbol(
      match[0],
      'Variable',
      vscode.SymbolKind.Variable,
      range,
      range
    )
  })
}

function getFunctionNames(document) {
  functions = [
    {
      type: 'Procedure',
      start: /^[ \t]*begin-procedure[ \t]+([\w-]+).*$/i,
      end: /^[ \t]*end-procedure.*$/i,
    },
    {
      type: 'Program',
      start: /^[ \t]*(begin-program).*$/i,
      end: /^[ \t]*end-program.*$/i,
    },
    {
      type: 'Setup',
      start: /^[ \t]*(begin-setup).*$/i,
      end: /^[ \t]*end-setup.*$/i,
    },
  ]
  const symbols = [];
  const functionStack = []
  const text = document.getText();
  for (let i = 0; i < document.lineCount; i++) {
    const line = document.lineAt(i);
    for (let func of functions) {
      let match = func.start.exec(line.text)
      if (match) {
        const name = match[1]
        functionStack.push({type: func.type, end: func.end, name: name, startPos: line.range.start})
      } else {
        if (functionStack.length > 0 && functionStack[functionStack.length - 1].end.exec(line.text)) {
          let fnEnd = functionStack.pop();
          let range = new vscode.Range(fnEnd.startPos, line.range.end);
          symbols.push(new vscode.DocumentSymbol(
            fnEnd.name,
            fnEnd.type,
            vscode.SymbolKind.Function,
            range,
            range
          ))
        }
      }
    }
  }
  return symbols;
}

module.exports = CustomSymbolProvider;