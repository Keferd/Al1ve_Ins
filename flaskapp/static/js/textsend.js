let sendbtn = document.querySelector(".main__run");

sendbtn.addEventListener("click", function (e) {
    e.preventDefault();

    text = document.getElementById("text_in").value
    let formdata = JSON.stringify({text: text});

    if (text != "") {
        fetch("/api/text",
        {
            method: "POST",
            body: formdata,
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then( response => {
            response.json().then(function(data) {
                predicted_class = data['class']
                weights = data['weights']
                new_text = ''

                const text_words = text.split(" ");

                    

                for (const word of text_words) {
                    if (word in weights) {
                        const weight = weights[word];
                        if (weight > 0.8) {
                            new_text += `<span style="color: white ;background-color: green">${word} </span> `;
                        } else if (weight > 0.6) {
                            new_text += `<span style="color: white ;background-color: blue">${word} </span> `;
                        } else if (weight > 0.4) {
                            new_text += `<span style="color: white ;background-color: purple">${word} </span> `;
                        }
                        else {
                            new_text += `${word} `
                        }
                    }
                    else {
                        new_text += `${word} `;
                    }
                }

                document.getElementById("text_out").innerHTML = new_text

                // -------------------------------- PDF --------------------------------
                // window.jsPDF = window.jspdf.jsPDF;
                // let doc = new jsPDF();
                // doc.setFont('tnr', 'normal');
                // // var textArray = doc.splitTextToSize(data, 180); 
                // // doc.text(textArray, 10, 10);
                // // doc.text(data, 10, 10);

                // var x = 10;
                // var y = 10;
                // var words = data.split(' ');
                // var line = '';

                // for (var i = 0; i < words.length; i++) {
                //     var testLine = line + words[i] + ' ';
                //     var testWidth = doc.getStringUnitWidth(testLine) * doc.internal.getFontSize();

                //     if (testWidth > 500) {
                //         doc.text(line, x, y);
                //         y += 8;

                //         if (y >= doc.internal.pageSize.height - 20) { 
                //             doc.addPage();
                //             y = 10; 
                //         }

                //         line = words[i] + ' ';
                //     } else {
                //         line = testLine;
                //     }
                // }

                // doc.text(line, x, y);



                // document.getElementById("main__file").innerHTML = `
                //     <a class="a_pdf" href=` + URL.createObjectURL(doc.output("blob")) + ` download="text.pdf">
                //         <div class="a_pdf__button">
                //             Скачать результат
                //         </div>
                //     </a>
                //     <style>
                //         .a_pdf {
                //             font-size: 18px;
                //             text-decoration: none;
                //         }

                //         .a_pdf__button {
                //             height: 40px;
                //             width: auto;
                //             padding: 0 20px;
                //             border: 1px solid #2c5dc7;
                //             color: #2c5dc7;
                //             border-radius: 20px;
                //             display: flex;
                //             align-items: center;
                //             justify-content: center;
                //             text-decoration: none;
                //         }

                //         .a_pdf__button:hover {
                //             text-decoration: underline;
                //         }
                //     </style>
                // `;
            })
        })
    }
    else {
        document.getElementById("text_in").placeholder = 'Введите текст'
    }
});