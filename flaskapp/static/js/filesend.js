let sendfilebtn = document.querySelector(".aside__button_submit");

sendfilebtn.addEventListener("click", function (e) {
    e.preventDefault();

    let input = document.getElementById("file");
    let file = input.files[0];
    
    let formdata = new FormData();
    formdata.append('file', file);
    formdata.append('test', 'test is work');


    if (typeof file != 'undefined') {
        fetch("/api/file",
        {
            method: "POST",
            body: formdata,
            /*headers: {
                'Content-Type': 'multipart/form-data'
            }*/
        })
        .then( response => {
            response.blob().then(function(data) {
                document.getElementById("download").innerHTML = `
                    <a class="aside__button_a" href=` + URL.createObjectURL(data) + ` download="table.xlsx">
                        <input class="aside__button_download" type="button" value="Скачать">
                    </a>
                `;
            });
        })
        .catch( error => {
            alert(error);
            console.error('error:', error);
        });
        
    }
    else {
        document.getElementById("download").innerHTML = `
            <div style="color: red; margin-left: 10px">
                Выберите файл
            </div>
        `
    }
});
