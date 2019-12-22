
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
    var transpose = $('#transpose-area input:radio:checked').val();
    var json = JSON.stringify({"file_name": file_name, "lyric": "None", "transpose": transpose});
    document.getElementById("lyrics-section").style.display = 'none';
    document.getElementById('txt').value = "";
    document.getElementById('txtarea').style.display = 'none';
    document.getElementsByClassName("container-fluid")[0].style.filter = "blur(8px)";
    document.getElementById("loading-section").style.display = "block";
    $.ajax({
        type: "POST",
        url: "http://0.0.0.0:5000/generate",
        data: json,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (response) {
            document.getElementById("loading-section").style.display = "none";
            Swal.fire(
                'Başarılı!',
                'Ses dosyası başarıyla oluşturuldu!',
                'success'
            );
            document.getElementById("lyrics-section").style.display = 'block';
            document.getElementById("lyrics-section").value = "Sözler:\n" + response.lyrics;
            document.getElementsByClassName("container-fluid")[0].style.filter = "blur(0px)";
            document.getElementById('mp3-player').innerHTML = "";
            document.getElementById('mp3-player').innerHTML = '<audio controls> <source src="static/generation/'+file_name+'.wav" type="audio/wav"></audio>';
        },
        error: function () {
            Swal.fire(
                'Başarısız!',
                'Bir şeyler yanlış gitti. Lütfen tekrar dene.',
                'error'
            );
        }
    });
}

function showtext()
{
    document.getElementById('mp3-player').innerHTML = "";
    document.getElementById("lyrics-section").style.display = 'none';
    document.getElementById('txtarea').style.display = 'block';
}

function hideText()
{
    document.getElementById('txtarea').style.display = 'none';
}

function generateWithLyrics()
{
    if(document.getElementById("txt").value == "")
    {
        Swal.fire('Başarısız!', 'Lütfen sözleri yazın.', 'error');
        return;
    }
    document.getElementById("lyrics-section").style.display = 'none';
    document.getElementById('mp3-player').innerHTML = "";
    var input = document.getElementById("txt").value;
    var file_name = randomName();
    var transpose = $('#transpose-area input:radio:checked').val();
    var json = JSON.stringify({"file_name": file_name, "lyric": input, "transpose": transpose});
    document.getElementById('txt').value = "";
    document.getElementById('txtarea').style.display = 'none';
    document.getElementsByClassName("container-fluid")[0].style.filter = "blur(8px)";
    document.getElementById("loading-section").style.display = "block";
    $.ajax({
        type: "POST",
        url: "http://0.0.0.0:5000/generate",
        data: json,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (response) {
            document.getElementById("loading-section").style.display = "none";
            Swal.fire(
                'Başarılı!',
                'Ses dosyası başarıyla oluşturuldu!',
                'success'
            );
            document.getElementById("lyrics-section").style.display = 'block';
            document.getElementById("lyrics-section").value = "Sözler:\n" + response.lyrics;
            document.getElementsByClassName("container-fluid")[0].style.filter = "blur(0px)";
            document.getElementById('mp3-player').innerHTML = '<audio controls> <source src="static/generation/'+file_name+'.wav" type="audio/wav"></audio>';
        },
        error: function () {
            Swal.fire(
                'Başarısız!',
                'Bir şeyler yanlış gitti. Lütfen tekrar dene.',
                'error'
            );
        }
    });
}