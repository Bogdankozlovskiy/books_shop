function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$("document").ready(function (){
    const csrftoken = getCookie('csrftoken');

    $(".like").on("click", function (){
        let id = $(this).attr("id")

        $.ajax(
            "http://localhost:8000/api_v1/add_like_to_comment_ajax/" + id + "/",
            {
                method: "POST",
                data: {"csrfmiddlewaretoken": csrftoken},
                success: function (data) {
                    console.log(data)
                    console.log("success")
                    $("#count_of" + id).html(data['likes'])
                },
                error: function (data) {
                    console.log(data)
                    console.log("errors")
                }
            }
        )
        console.log(id)

    })

})