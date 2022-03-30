// window.onload = function(){
//
// }
area1 = Array.from(document.getElementById('battlefield1').children)

var battlefield_user1 = [
    1, 1, 1, 1, 1, 1, 1, 1,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 0,
    0, 0, 0, 0, 0, 0, 1, 0,
    0, 0, 0, 0, 0, 0, 1, 0,
    0, 0, 0, 0, 0, 0, 1, 0,

]
$.ajax({
    url: '',
    type: 'GET',
    success: function (data) {
        battlefield_user1 = data.split(' ')
    },
})

for(var i = 0; i < 64; i++) {
    if(battlefield_user1[i] === 1)
    {
        $(area1)[i].style.backgroundColor = '#000'


    }
}
