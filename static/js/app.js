
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
    document.getElementById('transpose-area').style.display = 'none';
    document.getElementById('mp3-player').innerHTML = "";
    document.getElementById("loading-section").style.display = "block";
    $.ajax({
        type: "POST",
        //url: "http://3.231.61.200/generate",
        url: "http://0.0.0.0:8000/generate",
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
            document.getElementById('transpose-area').style.display = 'block';
            document.getElementById("lyrics-section").value = "Sözler:\n" + response.lyrics;
            document.getElementsByClassName("container-fluid")[0].style.filter = "blur(0px)";
            document.getElementById('mp3-player').innerHTML = '<audio controls> <source src="../static/generation/'+file_name+'.wav" type="audio/wav"></audio><a class="btn btn-outline-purple" href="../static/generation/'+file_name+'.wav" download="robotsinger.wav" style="margin-top: -30px; margin-left: 5px;"><i class="fas fa-file-download"></i></a>';
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
    document.getElementById('transpose-area').style.display = 'none';
    document.getElementById("loading-section").style.display = "block";
    $.ajax({
        type: "POST",
        //url: "http://3.231.61.200/generate",
        url: "http://0.0.0.0:8000/generate",
        data: json,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (response) {
            if(response.status_code == '400')
            {
                Swal.fire(
                    'Başarısız!',
                    'Daha kısa sözlerle tekrar deneyin!',
                    'error'
                );
                document.getElementById("loading-section").style.display = "none";
                document.getElementById('transpose-area').style.display = 'block';
                document.getElementsByClassName("container-fluid")[0].style.filter = "blur(0px)";
                return;
            }
            document.getElementById("loading-section").style.display = "none";
            Swal.fire(
                'Başarılı!',
                'Ses dosyası başarıyla oluşturuldu!',
                'success'
            );
            document.getElementById("lyrics-section").style.display = 'block';
            document.getElementById('transpose-area').style.display = 'block';
            document.getElementById("lyrics-section").value = "Sözler:\n" + response.lyrics;
            document.getElementsByClassName("container-fluid")[0].style.filter = "blur(0px)";
            document.getElementById('mp3-player').innerHTML = '<audio controls> <source src="../static/generation/'+file_name+'.wav" type="audio/wav"></audio><a class="btn btn-outline-purple" href="../static/generation/'+file_name+'.wav" download="robotsinger.wav" style="margin-top: -30px; margin-left: 5px;"><i class="fas fa-file-download"></i></a>';
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
