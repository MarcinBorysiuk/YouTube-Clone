function showReplies(ElementID) {
    var x = document.getElementById(ElementID);
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }

function writeReply(ElementID) {
var x = document.getElementById(ElementID);
if (x.style.display === "none") {
    x.style.display = "block";
} else {
    x.style.display = "none";
}
}

function change() // no ';' here
{
    var elem = document.getElementById("myButton");
    if (elem.value=="SHOW") elem.value = "HIDE";
    else elem.value = "SHOW";
}