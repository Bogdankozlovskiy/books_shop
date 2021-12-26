function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// https://youmightnotneedjquery.com/

$("document").ready(function (){
    const csrf_token = getCookie('csrftoken');

    $(".like").on("click", function (){
        let id = $(this).attr("id")
        let request = new XMLHttpRequest();
        request.open('POST', `http://localhost:8000/api_v1/add_like_to_comment_ajax/${id}/`, true);
        request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        request.onload = function (){
            $(`#count_of${id}`).html(JSON.parse(this.response)['likes'])
        }
        request.send(`csrfmiddlewaretoken=${csrf_token}`);
    })

})