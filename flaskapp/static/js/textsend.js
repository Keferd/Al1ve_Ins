let sendbtn = document.querySelector(".main__run");

sendbtn.addEventListener("click", function (e) {
    e.preventDefault();

    model = document.getElementById("model").value
    text = document.getElementById("text_in").value
    let formdata = JSON.stringify({text: text, model: model});

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
                categories = data['categories']
                new_text = ''

                const text_words = text.split(" ");

                let weights_list = ``;

                weights_list = `
                <div class="result__rating">Уровень рейтинга: <span class="result__rating_symbol">` + predicted_class + `</span></div>
                <div class="result__partition"></div>
                <div class="result__rating">Категория: <span class="result__rating_symbol">` + categories + `</span></div>
                <div class="result__partition"></div>
                <div class="result__header">
                    <div class="result__header_text">
                        Значение цветов:
                    </div>
                </div>
                <div class="result__classification">
                    <div class="result__point_span result__point_span_green">
                        Зелёный при значимости больше 0.8
                    </div>
                    <div class="result__point_span result__point_span_blue">
                        Синий при значимости больше 0.6
                    </div>
                    <div class="result__point_span result__point_span_purple">
                        Фиолетовый при значимости больше 0.4
                    </div>
                </div>
                <div class="result__header">
                    <div class="result__header_text">
                        Значимость слов:
                    </div>
                </div>
                <div class="result__lost_points">
                `;


                for (let id in weights) {
                    if (weights[id] > 0.4){
                        weights_list += `<div class="result__point"> ` + id + `:` + weights[id].toFixed(3) + `</div>`;
                    }
                }

                weights_list += `</div>`

                document.getElementById("results").innerHTML = weights_list;

                for (const word of text_words) {
                    l_word = word.toLowerCase()
                    if (l_word in weights) {
                        const weight = weights[l_word];
                        if (weight > 0.8) {
                            new_text += `<span class="result__point_span result__point_span_green">${word} </span> `;
                        } else if (weight > 0.6) {
                            new_text += `<span class="result__point_span result__point_span_blue">${word} </span> `;
                        } else if (weight > 0.4) {
                            new_text += `<span class="result__point_span result__point_span_purple">${word} </span> `;
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