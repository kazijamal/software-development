// demo 4
// JS event propagation

// Name the collections of TDs, TRs, and overall table
var tds = document.getElementsByTagName('td');
var trs = document.getElementsByTagName('tr');
var table = document.getElementsByTagName('table')[0];


var clicky = function(e) {
  alert( this.innerHTML );
  //Q: What will happen when next line is uncommented?
  //e.stopPropagation();
};


//Q: Does the order in which the event listeners are attached matter?

for (var x=0; x < tds.length; x++) {
  tds[x].addEventListener('click', clicky, true);
}

for (x=0; x < trs.length; x++) {
  trs[x].addEventListener('click', clicky, true);
}

table.addEventListener('click', clicky, true);

