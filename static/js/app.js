
function randomName()
{
    var anysize = 32;//the size of string 
    var charset = "abcdefghijklmnopqrstuvwxyz"; //from where to create
    var i=0, ret='';
    while(i++<anysize)
        ret += charset.charAt(Math.random() * charset.length)
    return ret;
}

function quickGeneration()
{
    var file_name = randomName();
    var json = JSON.stringify({"file_name": file_name, "lyric": "None"});
    document.getElementById("loader").style.display = "block";
    $.ajax({
        type: "POST",
        url: "http://0.0.0.0:5000/generate",
        data: json,
        contentType: "application/json; charset=utf-8",
        dataType: "text"
        }).done( function () {
            document.getElementById("loader").style.display = "none";
            Swal.fire(
                'Başarılı!',
                'Ses dosyası başarıyla oluşturuldu!',
                'success'
            );
            document.getElementById('mp3-player').innerHTML = "";
            document.getElementById('mp3-player').innerHTML = '<audio controls> <source src="static/generation/'+file_name+'.wav" type="audio/wav"></audio><p>Click the play button</p>';
    });
}

function showtext(){
     document.getElementById('txtarea').style.display = 'block';
}

function generateWithLyrics()
{
    if(document.getElementById("txt").value == "")
    {
        Swal.fire('Başarısız!', 'Lütfen sözleri yazın.', 'error');
        return;
    }
    var input = document.getElementById("txt").value;
    var file_name = randomName();
    var json = JSON.stringify({"file_name": file_name, "lyric": input});
    document.getElementById("loader").style.display = "block";
    $.ajax({
        type: "POST",
        url: "http://0.0.0.0:5000/generate",
        data: json,
        contentType: "application/json; charset=utf-8",
        dataType: "text"
        }).done( function () {
            document.getElementById("loader").style.display = "none";
            Swal.fire(
                'Başarılı!',
                'Ses dosyası başarıyla oluşturuldu!',
                'success'
            );
            document.getElementById('mp3-player').innerHTML = "";
            document.getElementById('mp3-player').innerHTML = '<audio controls> <source src="static/generation/'+file_name+'.wav" type="audio/wav"></audio><p>Click the play button</p>';
    });
}