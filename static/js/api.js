$.ajax("/info", {
    data:{symbols: 'AMZN, AAPL'},
    success: function(data) {
        console.log("success!");
        console.log(data);
    },
    error: function() {
        console.log("error :(");
    }
});
   
