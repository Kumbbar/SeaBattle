let area1 = Array.from(document.getElementById('battlefield1').children)
let area2 = Array.from(document.getElementById('battlefield2').children)
let area2_draw = document.getElementById('battlefield2')
let user1_move = true


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

// Get my battlefield
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


// Get enemy battlefield
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

// draw my battlefield
for(let i = 0; i < 64; i++)
{
    if(battlefield_user1[i] === 1)  $(area1)[i].style.backgroundColor = '#000';
    else if(battlefield_user1[i] === 2) $(area1)[i].style.backgroundColor = 'rgb(255,38,38)';
    else if(battlefield_user1[i] === 3) $(area1)[i].style.backgroundColor = 'rgb(160, 160, 160)';

}

// draw enemy battlefield
for(let i = 0; i < 64; i++)
{
    if(battlefield_user2[i] === 2)  $(area2)[i].style.backgroundColor = 'rgb(255,38,38)';
    else if(battlefield_user2[i] === 3) $(area2)[i].style.backgroundColor = 'rgb(160, 160, 160)';

}

area2_draw.addEventListener("click", function (e) {
    if(user1_move){
        let index = parseInt($(e.target).index());
        if(battlefield_user2[$(e.target).index()] === 1)
        {
            e.target.style.backgroundColor = 'rgb(255,38,38)';
            battlefield_user2[$(e.target).index()] = 2;
        }
        else
        {
            e.target.style.backgroundColor = 'rgb(160, 160, 160)';
            battlefield_user2[$(e.target).index()] = 3;
        }
        if(battlefield_user2.indexOf(1) ===  -1) window.location.href = '../win/';
        user1_move = false
        $.ajax({
            beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },

            type: "POST",
            url: '../interact_battlefield2/',
            data: {
                'battlefield': battlefield_user2.join(" ")
            },
            cache: false,



        })
        return 0
    }

})


// wait for enemy move and draw after

setInterval(function () {
    if(!user1_move)
    {
        $.ajax({
            url: '../interact_battlefield1/',
            type: 'GET',
            async: false,
            success: function (data) {
                let battlefield1_check = data.split(' ')
                battlefield1_check = battlefield1_check.map(function (item) {
                    return parseInt(item);
                })
                if(battlefield_user1.toString() !== battlefield1_check.toString()) {


                    battlefield_user1 = battlefield1_check
                    if(battlefield_user1.indexOf(1) ===  -1) window.location.href = '../lose/'
                    for(let i = 0; i < 64; i++)
                    {
                        if(battlefield_user1[i] === 1)  $(area1)[i].style.backgroundColor = '#000';
                        else if(battlefield_user1[i] === 2) $(area1)[i].style.backgroundColor = 'rgb(255,38,38)';
                        else if(battlefield_user1[i] === 3) $(area1)[i].style.backgroundColor = 'rgb(160, 160, 160)';

                    }
                    user1_move = true;
                }

            }
        })

    }
    
},2000)




