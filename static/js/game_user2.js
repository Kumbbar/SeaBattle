
let area1 = Array.from(document.getElementById('battlefield1').children)
let area2 = Array.from(document.getElementById('battlefield2').children)
let area2_draw = document.getElementById('battlefield2')
let user2_move = false


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

let battlefield_user1 = [
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,

]

let battlefield_user2 = [
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,

]

$.ajax({
    url: '../interact_battlefield1/',
    type: 'GET',
    async: false,
    success: function (data) {
        battlefield_user1 = data.split(' ');
        battlefield_user1 = battlefield_user1.map(function (item) {
            return parseInt(item);
        })
    },
})

$.ajax({
    url: '../interact_battlefield2/',
    type: 'GET',
    async: false,
    success: function (data) {
        battlefield_user2 = data.split(' ');
        battlefield_user2 = battlefield_user2.map(function (item) {
            return parseInt(item);
        })
    },
})


for(let i = 0; i < 64; i++)
{
    if(battlefield_user1[i] === 1)  $(area1)[i].style.backgroundColor = '#000';
    else if(battlefield_user1[i] === 0);

}

for(let i = 0; i < 64; i++)
{
    if(battlefield_user2[i] === 1)  $(area2)[i].style.backgroundColor = '#000';
    else if(battlefield_user2[i] === 0);

}

area2_draw.addEventListener("click", function (e) {
    if(user2_move){
        let index = parseInt($(e.target).index());
        battlefield_user1[$(e.target).index()] = 1;
        e.target.style.backgroundColor = '#000';
        user2_move = false
        $.ajax({
            beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },

            type: "POST",
            url: '../interact_battlefield1/',
            data: {
                'battlefield': battlefield_user1.join(" ")
            },
            cache: false,



        })
        return 0
    }

})


// wait for enemy move and draw after

setInterval(function () {
    if(!user2_move)
    {
        $.ajax({
            url: '../interact_battlefield2/',
            type: 'GET',
            async: false,
            success: function (data) {
                let battlefield2_check = data.split(' ')
                battlefield2_check = battlefield2_check.map(function (item) {
                    return parseInt(item);
                })
                if(battlefield_user2.toString() !== battlefield2_check.toString()) {


                    battlefield_user2 = battlefield2_check
                    for(let i = 0; i < 64; i++)
                    {
                        if(battlefield_user2[i] === 1)  $(area2)[i].style.backgroundColor = '#000';
                        else if(battlefield_user2[i] === 0);

                    }
                    user2_move = true;
                }

            }
        })

    }

},2000)




