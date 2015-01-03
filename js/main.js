$(document).ready(Main);

function getParameter(name) {
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
        if (pair[0] == name) {
            return pair[1];
        }
    } 
}
function dateConverter(UNIX_TIMESTAMP){
    var a = new Date(UNIX_TIMESTAMP * 1000);
    var year = a.getFullYear();
    var month = a.getMonth();
    var day = a.getDate();
    var newDate = new Date(year, month, day);
    return newDate;
}

function Main(){
    var timestamp = getParameter("currenttime");
    var current_date = dateConverter(timestamp);
    var target_year = current_date.getFullYear()+1;
    var target_date = new Date(target_year, 0, 1);
    var temp_date = target_year.toString() + " January 1st";
    $.getScript("js/countdown.js", function(){
        var clock = document.getElementById("countdown"), targetDate = new Date(target_year, 00, 01); // Jan 1, 2050
        clock.innerHTML = countdown(targetDate).toString() + " till " + temp_date.fontcolor("#1ABC9C");
        setInterval(function(){
            clock.innerHTML = countdown(targetDate).toString() + " till " + temp_date.fontcolor("#1ABC9C");
        }, 1000);
    });
}