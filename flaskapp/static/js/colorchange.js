function highlightWords() {
    const inputText = document.getElementById("inputText").value;
    const outputText = document.getElementById("outputText");

    if (inputText) {
        const words = inputText.split(" ");

        let outputHtml = "";

        for (const word of words) {
            const color = getWordColor(word);
            outputHtml += `<span class="${color}">${word} </span>`;
        }

        outputText.innerHTML = outputHtml;
    } else {
        outputText.innerHTML = "";
    }
}

function getWordColor(word) {
    if (word in weights_dict) {
        const weight = weights_dict[word];
        if (weight > 0.8) {
            return 'green';
        } else if (weight > 0.6) {
            return 'blue';
        } else if (weight > 0.4) {
            return 'purple';
        }
    }

    return "";
}
