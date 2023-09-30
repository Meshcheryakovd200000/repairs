let alertWrapper = document.querySelector('.alert');
let alertClose = document.querySelectorAll('.alert__close');


if (alertWrapper) {
    for(let i=0; i < alertClose.length; i++){
    alertClose[i].addEventListener('click', function(){
        this.parentNode.remove();
    })
    }
}

//if (alertWrapper) {
//  alertClose.addEventListener('click', () =>
//    alertWrapper.style.display = 'none'
//)}


//alertClose.forEach(function (item) {
//    item.addEventListener('click', function () {
//        parentModal = this.closest('.alert');
//        parentModal.style.display = 'none';
//    });
//});






















