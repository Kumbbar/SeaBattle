$.ajax({
    url: 'check_user_game/',
    type: 'GET',
    async: false,
    success: function (data) {
        if(data === 'false') localStorage.clear();
    },
    cache: false
})
