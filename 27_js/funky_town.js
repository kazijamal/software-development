var foo = function() {
    console.log("foo testing");
}

var factorial = function(n) {
    if (n == 1) {
	return 1;
    }
    return n * factorial(n-1);
}

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
    min = a < b ? a : b;
    i = 0;
    while (i < min) {
	if (a % i == 0 && b % i == 0) {
	    i++;
	} else {
	    i = i^2;
	};
    }
    console.log(i);
    return i;
}
