// window.onload = function(){
//
// }
area1 = Array.from(document.getElementById('battlefield1').children)
let user1_move = true

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
for(let i = 0; i < 64; i++)
        {
            if(battlefield_user1[i] === 1)  $(area1)[i].style.backgroundColor = '#000';
            else if(battlefield_user1[i] === 0);

        }




