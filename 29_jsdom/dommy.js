var changeHeading = function(e) {
    var h = document.getElementById("h");
    h.innerHTML = e;
};

var removeItem = function(e) {
    e.remove();
};

var lis = document.getElementsByTagName("li");
var count = lis.length
 
for (var i=0; i < lis.length; i++) {
    lis[i].addEventListener('mouseover',
			    function(e) { changeHeading(e['target'].innerHTML); });
    lis[i].addEventListener('mouseout',
			    function(e) { changeHeading("Hello World!"); });
    lis[i].addEventListener('click',
			    function(e) { removeItem(e['target']); });
};

var addItem = function(e) {
    console.log(e);
    var list = document.getElementById("thelist");
    var item = document.createElement("li");
    item.innerHTML = "item " + count++;
    item.addEventListener('mouseover',
			    function(e) { changeHeading(e['target'].innerHTML); });
    item.addEventListener('mouseout',
			    function(e) { changeHeading("Hello World!"); });
    item.addEventListener('click',
			    function(e) { removeItem(e['target']); });
    list.appendChild(item);
};

var button = document.getElementById("b");
button.addEventListener('click', addItem);

var fnum = 0;

var fib = function(n) {
    if (n < 2) {
	return 1;
    }
    else {
	return fib(n-1) + fib(n-2);
    }
};

var addFib = function(e) {
    console.log(e);
    var list = document.getElementById("fiblist");
    var item = document.createElement("li");
    item.innerHTML = fib(fnum++);
    list.appendChild(item);
}

var addFib2 = function(e) {
    console.log(e);
}

var fb = document.getElementById("fb");
fb.addEventListener('click', addFib);
