// Biraj Chowdhury & Kazi Jamal
// SoftDev1 pd9
// K28 -- Sequential Progression II: Electric Boogaloo
// 2019-12-12

var foo = function() {
    console.log("foo testing");
};

var factorial = function(n) {
    if (n <= 1) {
	return 1;
    }
    return n * factorial(n-1);
};

var fibonacci = function(n) {
    if (n == 0) {
	return 0;
    };
    if (n == 1) {
	return 1;
    };
    return fibonacci(n-1) + fibonacci(n-2);
};

var gcd = function(a, b) {
    if (a == 0 || b == 0) {
	return "a or b cannot be 0";
    };
    if (b > a) {
	return gcd(b, a);
    };
    if (a % b == 0) {
	return b;
    };
    gcd(b, a % b);
};
	    
var students = ["kazi", "albert", "nahi", "john", "jane"];

var randomStudent = function(students) {
    var randIndex = Math.floor(Math.random() * students.length);
    return students[randIndex];
};

var printFib = function() {
    var ans = fibonacci(8)
    console.log(ans);
    return ans;
};

var fibbtn = document.getElementById("fibbtn");
fibbtn.addEventListener('click', printFib);
