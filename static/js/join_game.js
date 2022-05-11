var area = document.getElementById('battlefield');
var boxes = document.getElementsByClassName('cell');
var box = document.querySelectorAll('.cell');
var reset = document.querySelector('.reset')
var ships = 14;
var play = document.querySelector('.play')

if(localStorage.getItem('move2') === null)  localStorage.setItem('move2', 'false');



var battlefield_ready = [
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,

]

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


var csrftoken = getCookie('csrftoken');


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

reset.addEventListener('click', function (e) {
    window.location.reload();
})

play.addEventListener('click', function (e) {
    $.ajax({
        beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
        type: "POST",
        url: '../game_user2/',
        data: {
            'battlefield': battlefield_ready.join(" ")
        },
        cache: false,

        success: function (data) {
            window.location.href = '../game_user2/';

        }

    })
})

area.addEventListener("click", function (e) {
    var index = parseInt($(e.target).index());
    console.log(index)
    if (battlefield_ready[index] === 1) return 0;
    if (ships > 0) {

        // left
        if ([0, 8, 16, 24, 32, 40, 48, 56].includes(index)) {
            console.log("lest")
            if (index + 9 > 64) {
                if (battlefield_ready[index - 7] === 0) {
                    battlefield_ready[$(e.target).index()] = 1;
                    e.target.style.backgroundColor = '#000';
                    ships--;
                }
            } else if (battlefield_ready[index + 9] === 0) {
                battlefield_ready[$(e.target).index()] = 1;
                e.target.style.backgroundColor = '#000';
                ships--;
            }
        }

        // top
        else if ([1, 2, 3, 4, 5, 6].includes(index)) {
            console.log("topp")
            if (battlefield_ready[index + 7] === 0 && battlefield_ready[index + 9] === 0) {
                battlefield_ready[$(e.target).index()] = 1;
                e.target.style.backgroundColor = '#000';
                ships--;
            }
        }

        // right
        else if ([7, 15, 23, 31, 39, 47, 55, 63].includes(index)) {
            console.log('right')
            if (index + 7 > 64) {
                if (battlefield_ready[index - 9] === 0) {
                    battlefield_ready[$(e.target).index()] = 1;
                    e.target.style.backgroundColor = '#000';
                    ships--;
                }
            } else if (battlefield_ready[index + 7] === 0) {
                battlefield_ready[$(e.target).index()] = 1;
                e.target.style.backgroundColor = '#000';
                ships--;
            }
        }

        // bottom
        else if ([57, 58, 59, 60, 61, 62].includes(index)) {
            if (battlefield_ready[index - 7] === 0 && battlefield_ready[index - 9] === 0) {
                battlefield_ready[$(e.target).index()] = 1;
                e.target.style.backgroundColor = '#000';
                ships--;
            }
        } else if (battlefield_ready[index - 9] === 0
            && battlefield_ready[index - 7] === 0
            && battlefield_ready[index + 7] === 0
            && battlefield_ready[index + 9] === 0
        ) {
            console.log('enter')
            battlefield_ready[$(e.target).index()] = 1;
            e.target.style.backgroundColor = '#000';
            ships--;
        }
    }

    if (ships == 10) document.getElementById('ship4').style.backgroundColor = 'rgb(160, 160, 160)';
    else if (ships == 7) document.getElementById('ship3').style.backgroundColor = 'rgb(160, 160, 160)';
    else if (ships == 5) document.getElementById('ship21').style.backgroundColor = 'rgb(160, 160, 160)';
    else if (ships == 3) document.getElementById('ship22').style.backgroundColor = 'rgb(160, 160, 160)';
    else if (ships == 2) document.getElementById('ship11').style.backgroundColor = 'rgb(160, 160, 160)';
    else if (ships == 1) document.getElementById('ship12').style.backgroundColor = 'rgb(160, 160, 160)';
    else if (ships == 0) document.getElementById('ship13').style.backgroundColor = 'rgb(160, 160, 160)';
    //console.log($(event.target).index());
    //$(event.target).toggle.style.backgroundColor = "#101010";
    //$(event.target).style.backgroundColor = "rgb(0, 0, 0)";
});
