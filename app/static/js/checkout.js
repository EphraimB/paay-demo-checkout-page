var id = document.querySelector('[data-threeds=id]');
var uniqueId = function() {
    return 'id-' + Math.random().toString(36).substr(2, 16);
};
id.value = uniqueId();

var tds = new ThreeDS("billing-form", "{{ apiKey }}",null,{verbose:true});
var nResponse = function(nResponse){
    $("#console").find("div.card-body").append("<p>User got prompted. Card has NOT been authenticated!</p>")
    $("div.modal-body").append("<p>Card has could not been authenticated. For best results please use a Visa or Mastercard Rewards card.</p>")
}

$("[data-threeds]").on("change", function() {
    var readyState = 1;
    $("[data-threeds]").each(function() {
        if (!$(this).val()) {
            readyState = 0
        }
    });
    if (readyState) {
        $("#console").find("div.card-body").append("<p>...authenticating...</p>")
        var notAuthenticated = setTimeout(function() {nResponse();}, 20000)
        tds.verify(function(sResponse){
            if(sResponse.status === "Y"|| sResponse.status === "A"){
                clearTimeout(notAuthenticated);
                $("#console").find("div.card-body").append("<p>Card has been authenticated!</p>")
                $("div.modal-body").append("<p class='text-center'>Card has been authenticated!</p>")
                if (sResponse.protocolVersion == "2.1.0"){
                    $("ul.list-group-modal").append("<li class='list-group-item d-flex justify-content-between'><span>ACS ID</span><strong>" + sResponse.acsTransId + "</strong></li>")
                    $("ul.list-group-modal").append("<li class='list-group-item d-flex justify-content-between'><span>Authentication Value</span><strong>" + sResponse.authenticationValue + "</strong></li>")
                    $("ul.list-group-modal").append("<li class='list-group-item d-flex justify-content-between'><span>DS Transaction ID</span><strong>" + sResponse.dsTransId + "</strong></li>")
                    $("ul.list-group-modal").append("<li class='list-group-item d-flex justify-content-between'><span>ECI</span><strong>" + sResponse.eci + "</strong></li>")
                    $("ul.list-group-modal").append("<li class='list-group-item d-flex justify-content-between'><span>Protocol Version</span><strong>" + sResponse.protocolVersion + "</strong></li>")
                    $("ul.list-group-modal").append("<li class='list-group-item d-flex justify-content-between'><span>Status</span><strong>" + sResponse.status+ "</strong></li>")
                }
                else {
                    $("ul.list-group-modal").append("<li class='list-group-item d-flex justify-content-between'><span>CAVV</span><strong>" + sResponse.cavv+ "</strong></li>")
                    $("ul.list-group-modal").append("<li class='list-group-item d-flex justify-content-between'><span>XID</span><strong>" + sResponse.xid+ "</strong></li>")
                    $("ul.list-group-modal").append("<li class='list-group-item d-flex justify-content-between'><span>ECI</span><strong>" + sResponse.eci + "</strong></li>")
                    $("ul.list-group-modal").append("<li class='list-group-item d-flex justify-content-between'><span>Status</span><strong>" + sResponse.status+ "</strong></li>")
                }

            } else if (sResponse.status === "N"||sResponse.status === "U") {
                clearTimeout(notAuthenticated);
                $("#console").find("div.card-body").append("<p>Card has NOT been authenticated!</p>")
                $("div.modal-body").append("<p>Card has could not been authenticated. For best results please use a Visa or Mastercard Rewards card.</p>")
            }
        },function(fResponse){
            clearTimeout(notAuthenticated);
            $("#console").find("div.card-body").append("<p>Card has NOT been authenticated!</p>")
            $("div.modal-body").append("<p>Card has could not been authenticated. For best results please use a Visa or Mastercard Rewards card.</p>")
        },{
            amount:8
        })
    }
});