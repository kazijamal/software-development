var foo = function() {
    console.log("foo testing");
};

foo()

var factorial = function(n) {
    if (n <= 1) {
	return 1;
    }
    return n * factorial(n-1);
};

console.log(factorial(1));
console.log(factorial(2));
console.log(factorial(3));
console.log(factorial(4));
console.log(factorial(5));

var fibonacci = function(n) {
    if (n == 0) {
	return 0;
    };
    if (n == 1) {
	return 1;
    };
    return fibonacci(n-1) + fibonacci(n-2);
};

console.log(fibonacci(0));
console.log(fibonacci(1));
console.log(fibonacci(2));
console.log(fibonacci(3));
console.log(fibonacci(4));
console.log(fibonacci(5));

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
    return gcd(b, a % b);
};

console.log(gcd(18,3));
console.log(gcd(3,18));
console.log(gcd(0,0));
console.log(gcd(48,18));
	    
var students = ["kazi", "albert", "nahi", "john", "jane"];

var randomStudent = function(students) {
    var randIndex = Math.floor(Math.random() * students.length);
    return students[randIndex];
};

console.log(randomStudent(students));
console.log(randomStudent(students));
console.log(randomStudent(students));
console.log(randomStudent(students));
console.log(randomStudent(students));
