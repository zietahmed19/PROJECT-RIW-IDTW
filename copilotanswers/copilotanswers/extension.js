const vscode = require('vscode');
const fs = require('fs');

// Function to read Stack Overflow questions from the CSV file
function readStackOverflowQuestions(csvFilePath) {
    const questions = [];
    const fileContent = fs.readFileSync(csvFilePath, 'utf-8');
    const lines = fileContent.split('\n');
    for (const line of lines) {
        const columns = line.split(',');
        if (columns.length >= 2) {
            questions.push(columns[1].trim());
        }
    }
    return questions;
}

// Function to generate answers using GitHub Copilot
async function generateAnswers(questions) {
    const answers = {};
    for (const question of questions) {
        const answer = await vscode.commands.executeCommand('vscode-copilot.generate', question);
        if (answer) {
            answers[question] = answer;
        }
    }
    return answers;
}

// Function to write answers to a file
function writeAnswersToFile(answers, outputFilePath) {
    const outputText = JSON.stringify(answers, null, 2);
    fs.writeFileSync(outputFilePath, outputText, 'utf-8');
}

// Activate the extension
function activate(context) {
    const disposable = vscode.commands.registerCommand('extension.generateAnswers', async () => {
        const csvFilePath = vscode.workspace.getConfiguration().get('extension.csvFilePath');
        if (!csvFilePath) {
            vscode.window.showErrorMessage('CSV file path not configured.');
            return;
        }

        const questions = readStackOverflowQuestions(csvFilePath);
        const answers = await generateAnswers(questions);

        const outputFilePath = vscode.workspace.getConfiguration().get('extension.outputFilePath');
        if (!outputFilePath) {
            vscode.window.showErrorMessage('Output file path not configured.');
            return;
        }

        writeAnswersToFile(answers, outputFilePath);

        vscode.window.showInformationMessage('Answers generated and saved.');
    });

    context.subscriptions.push(disposable);
}

module.exports = {
    activate
};
