async function elementUpdate(selector) {
    try {
        var html = await (await fetch(location.href)).text();
        var newdoc = new DOMParser().parseFromString(html, 'text/html');
        document.querySelector(selector).outerHTML = newdoc.querySelector(selector).outerHTML;
        console.log('Элемент ' + selector + ' был успешно обновлен');
        return true;
    } catch (err) {
        console.log('При обновлении элемента ' + selector + ' произошла ошибка:');
        console.dir(err);
        return false;
    }
}

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

window.onload = function () {
    let h1 = document.querySelector('.create-game');
    h1.addEventListener('click', function () {
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            type: 'POST',
            url: 'ajax/',
            data: {
                'username': 'Dima',
            },
            cache: false,

            dataType: 'text',
            complete: function (data) {

            }


        })

    })
}