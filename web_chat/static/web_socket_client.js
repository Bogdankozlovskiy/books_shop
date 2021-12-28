document.addEventListener("DOMContentLoaded", function (){
    function connect(){
        let socket = new WebSocket("ws://localhost:8765")

        socket.onmessage = function (message) {
            let response_data = JSON.parse(message.data)  // make json dictfrom string
            let message_tag_text = document.createElement("h3")
            message_tag_text.innerHTML = response_data['text']

            let message_tag_date = document.createElement("h3")
            message_tag_date.innerHTML = response_data['date']

            let message_container = document.querySelector("#message-container")
            message_container.append(message_tag_text)
            message_container.append(message_tag_date)
            message_container.append(document.createElement("hr"))
        }
        let submit_button = document.querySelector("#submit-button")
        submit_button.addEventListener("click", function () {
            let text_area = document.querySelector("[name=text]")
            socket.send(text_area.value)
            text_area.value = ''
        }, false)
        socket.onclose = function (){
            socket = null
            setTimeout(connect, 1000)
        }
    }
    connect()
}, false)
