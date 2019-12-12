var changeHeading = function(e) {
    var h = document.getElementById("h");
    h.innerHTML = e;
};

var removeItem = function(e) {
    lis.splice(index, e);
};

var lis = document.getElementsByTagName("li");
 
for (var i=0; i < lis.length; i++) {
    lis[i].addEventListener('mouseover',
			    function(e) { changeHeading(e['target'].innerHTML); });
    lis[i].addEventListener('mouseout',
			    function(e) { changeHeading("Hello World!"); });
    lis[i].addEventListener('click',
			    function(e) { removeItem(i); });
}
