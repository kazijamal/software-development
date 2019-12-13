// changes heading on top of webpage to e
var changeHeading = function(e) {
    var h = document.getElementById("h");
    h.innerHTML = e;
};

// removes item from list
var removeItem = function(e) {
    e.remove();
};

// creates list from the list in html
var lis = document.getElementsByTagName("li");
var count = lis.length

// adds event listeners to all elements of the list
for (var i=0; i < lis.length; i++) {
    lis[i].addEventListener('mouseover',
			    function() { changeHeading(this.innerHTML); });
    lis[i].addEventListener('mouseout',
			    function() { changeHeading("List Demo"); });
    lis[i].addEventListener('click',
			    function() { removeItem(this); });
};

// adds item to list
var addItem = function(e) {
    console.log(e);
    var list = document.getElementById("thelist");
    var item = document.createElement("li");
    item.innerHTML = "item " + count++;
    item.addEventListener('mouseover',
			    function() { changeHeading(this.innerHTML); });
    item.addEventListener('mouseout',
			    function() { changeHeading("Hello World!"); });
    item.addEventListener('click',
			    function() { removeItem(this); });
    list.appendChild(item);
};

// adds listener to button for adding item to the list
var button = document.getElementById("b");
button.addEventListener('click', addItem);

var fnum = 0;

// calculates nth number of fibonacci sequence
var fib = function(n) {
    if (n < 2) {
	return 1;
    }
    else {
	return fib(n-1) + fib(n-2);
    }
};

// adds next fibonacci number to fibonacci list
var addFib = function(e) {
    console.log(e);
    var list = document.getElementById("fiblist");
    var item = document.createElement("li");
    item.innerHTML = fib(fnum++);
    list.appendChild(item);
}

// adds listener to button for adding item to fibonacci list
var fb = document.getElementById("fb");
fb.addEventListener('click', addFib);

var factnum = 1;

// calculates n factorial
var fact = function(n) {
    if (n <= 1) {
	return 1;
    }
    else {
	return n * fact(n-1);
    }
};

// adds next factorial to factorial list
var addFact = function(e) {
    console.log(e);
    var list = document.getElementById("factlist");
    var item = document.createElement("li");
    item.innerHTML = fact(factnum++);
    list.appendChild(item);
}

// adds listener to button for adding item to factorial list
var factb = document.getElementById("factb");
factb.addEventListener('click', addFact);

// xtra
var lastFib = function(e) {
    while (fnum < 40) {
	addFib();
    }
};

var flastb = document.getElementById("flastb");
flastb.addEventListener('click', lastFib);

var lastFact = function(e) {
    while (factnum < 172) {
	addFact();
    }
};

var factlastb = document.getElementById("factlastb");
factlastb.addEventListener('click', lastFact);
