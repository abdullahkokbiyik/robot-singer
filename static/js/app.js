
function quickGeneration()
{
    $.ajax({
        type: "POST",
        url: "http://0.0.0.0:5000/generate/test",
        data: {file_name: "test"},
        dataType: "text"
        }).done( function () {
            Swal.fire("success", "Ses dosyası başarıyla oluşturuldu!");
            document.getElementById('mp3-player').innerHTML = '<audio controls> <source src="static/generation/test.wav" type="audio/wav"></audio><p>Click the play button</p>';
    });
}