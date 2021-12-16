$("document").ready(function (){

    $(".like").on("click", function (){
        let id = $(this).attr("id")

        $.ajax(
            "http://localhost:8000/shop/add_like_to_comment_ajax/" + id + "/",
            {
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