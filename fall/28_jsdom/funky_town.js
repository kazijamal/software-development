// Biraj Chowdhury & Kazi Jamal
// SoftDev1 pd9
// K28 -- Sequential Progression II: Electric Boogaloo
// 2019-12-12

// foo function for testing
var foo = function() {
    console.log("foo testing");
};

// returns factorial of n
var factorial = function(n) {
    if (n <= 1) {
	return 1;
    }
    return n * factorial(n-1);
};

// returns nth number in the fibonacci sequence
var fibonacci = function(n) {
    if (n == 0) {
	return 0;
    };
    if (n == 1) {
	return 1;
    };
    return fibonacci(n-1) + fibonacci(n-2);
};

// returns greatest common divisor of a and b
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

// list of students for testing
var students = ["biraj", "kazi", "albert", "nahi","john", "jane"];

// returns a random student from a list of students
var randomStudent = function(students) {
    var randIndex = Math.floor(Math.random() * students.length);
    return students[randIndex];
};

// logs factorial(7) to console and displays answer
var facttest = function() {
    var ans = factorial(7);
    console.log(ans);
    document.getElementById('factans').innerHTML = "factorial(7) = " + ans;
};

// calls facttest when button with id factbtn is clicked
var factbtn = document.getElementById('factbtn');
factbtn.addEventListener('click', facttest);

// logs fibonacci(8) to console and displays answer
var fibtest = function() {
    var ans = fibonacci(8);
    console.log(ans);
    document.getElementById('fibans').innerHTML = "fibonacci(8) = " + ans;
};

// calls fibtest when button with id fibbtn is clicked
var fibbtn = document.getElementById('fibbtn');
fibbtn.addEventListener('click', fibtest);

// logs gcd(1115,45) to console and displays answer
var gcdtest = function() {
    var ans = gcd(1115,45);
    console.log(ans);
    document.getElementById('gcdans').innerHTML = "gcd(1115,45) = " + ans;
};

// calls gcdtest when button with id gcdbtn is clicked
var gcdbtn = document.getElementById('gcdbtn');
gcdbtn.addEventListener('click', gcdtest);

// logs randomStudent(students) to console and displays students list and answer
var randtest = function() {
    var ans = randomStudent(students);
    console.log(ans);
    document.getElementById('students').innerHTML = "List of students: " + students;
    document.getElementById('randans').innerHTML = "Random student: " + ans;
};

// calls randtest when button with id randbtn is clicked
var randbtn = document.getElementById('randbtn');
randbtn.addEventListener('click', randtest);
