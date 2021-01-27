let stratBox = {
    init: function (){
        stratBox.apiGet("/cache/"+"strat"+"/bull/", (response) => {
            stratBox.fillTheBox(response, "bull");
        })
        stratBox.apiGet("/cache/"+"strat"+"/bear/", (response) =>{
            stratBox.fillTheBox(response, "bear");
        })
    },
    fillTheBox: function (data, side) {
        stratHTML = `<tbody>
                        <tr>
                            <td>${data[0].rsi}</td>
                            <td>${data[0].sma}</td>
                            <td>${data[0].trend}</td>
                        </tr>
                    </tbody>`;
        let insertTarget;
        if (side === "bull"){
            insertTarget = document.querySelector("#bullStratBoxHead");
            insertTarget.nextElementSibling.remove();
        }
        if (side === "bear") {
            insertTarget = document.querySelector("#bearStratBoxHead");
            insertTarget.nextElementSibling.remove();
        }
        insertTarget.insertAdjacentHTML("afterend", stratHTML);
        console.log("refresh")
        },
    apiGet: function (url, callback){
        fetch(url, {
            method: "GET",
            credentials: "same-origin"
        })
            .then(response => response.json())
            .then(json_response => callback(json_response));
    },
}
stratBox.init();
setInterval(stratBox.init, 60000);
