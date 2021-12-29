var pollWorkflow = null;
var currentWorkflowId = null;
var status_out = null;
var workflow_type = null;
var expense_data = null;

var kvm_workflowId = null;

let workflowDiffAId = null;
let workflowDiffBId = null;
let workflowDiffTimeAId = null;
let workflowDiffTimeBId = null;

var dataSet = nil;

$(document).ready(function () {
	// expense_table.php will be used to send the data to the sever database
	$('#example-1').Tabledit({
		url: '',
		editButton: false,
		deleteButton: false,
		hideIdentifier: true,
		columns: {
			identifier: [0, 'id'],
			editable: [[2, 'first'], [3, 'last'], [3, 'nickname']]
		}
	});

});
$(document).ready(function () {
	$('#expense_table').DataTable({
		"aaSorting": [],
		columnDefs: [{
			orderable: false,
			targets: 3
		}]
	});
	$('.dataTables_length').addClass('bs-select');
});

function tableRowProcessor(row) {
	var row_data = row.cells;
	console.log(row_data[0].innerHTML);
	processMonthEntry(row_data[0].innerHTML);
}

function processMonthEntry(month) {
	console.log('Inside process month entry')
	axios.post(
		'/data_query', json = { 'month': month }
	).then((response) => {
		expense_data = response.data;
		expense_data = createDataset(expense_data);
		console.log(expense_data);
		createExpenseTable(expense_data);
	})
		.catch((error) => {
			console.log('error ' + error);
		});

}

function createDataset(expense_data) {
	var dataSet = [];
	for (var i = 0; i < expense_data.length; i++) {
		dataSet.push(
			[
				"<input type='checkbox' name='ips' checked>",
				i,
				expense_data[i].source,
				expense_data[i].transaction_date,
				expense_data[i].transaction_store,
				expense_data[i].transaction_amount
			]
		)
	}
	return dataSet
}
function createExpenseTable(expense_data) {
	// 	var headerList = ["Select", "S. No", "Source", "Transaction Data", "Transaction Store", "Transaction Amount"];
	$('#expense_table').DataTable({
		bDestroy: true,
		data: expense_data,
		columns: [
			{ title: "Select" },
			{ title: "Serial" },
			{ title: "Source" },
			{ title: "Transaction Data" },
			{ title: "Transaction Store" },
			{ title: "Transaction Amount" }
		]
	});
}


// function createExpenseTable(expense_data) {
// 	var head = document.getElementsByTagName('head')[0];
// 	var link = document.createElement('link');
// 	link.rel = 'stylesheet';
// 	link.type = 'text/css';
// 	link.href = 'https://cdn.datatables.net/1.11.3/css/jquery.dataTables.min.css';
// 	link.media = 'all';
// 	head.appendChild(link);

// 	var tdoc = document.getElementById('imsg');
// 	document.getElementById("imsg").type = "table";

// 	while (tdoc.hasChildNodes()) {
// 		tdoc.removeChild(tdoc.firstChild);
// 	}
// 	//document.getElementById("kvm_list_table").style.display = "";
// 	//	<table id="jira_list" class="table" style="width:60%">
// 	tbl = document.createElement('table');
// 	tbl.style.width = '60%';
// 	tbl.id = 'expense_table';
// 	tbl.setAttribute('class', "table table-striped table-bordered table-sm");
// 	console.log(expense_data);
// 	// Header 

// 	var tr = document.createElement('tr'); // Header row
// 	var headerList = ["Select", "S. No", "Source", "Transaction Data", "Transaction Store", "Transaction Amount"];
// 	for (var j = 0; j < headerList.length; j++) {
// 		var th = document.createElement('th'); //column
// 		var text = document.createTextNode(headerList[j]); //cell
// 		th.appendChild(text);
// 		th.setAttribute('class', 'th-sm');
// 		tr.appendChild(th);
// 	}
// 	tbl.appendChild(tr);

// 	for (var i = 0; i < expense_data.length; i++) {

// 		var newRow = document.createElement('tr');
// 		newRow.insertCell(0).innerHTML = "<input type='checkbox' name='ips' checked>"
// 		newRow.insertCell(1).appendChild(document.createTextNode(i)); //S. No
// 		newRow.insertCell(2).appendChild(document.createTextNode(expense_data[i].source)); // KVM FQDN
// 		newRow.insertCell(3).appendChild(document.createTextNode(expense_data[i].transaction_date)); // POP
// 		newRow.insertCell(4).appendChild(document.createTextNode(expense_data[i].transaction_store)); // CPU Avail
// 		newRow.insertCell(5).appendChild(document.createTextNode(expense_data[i].transaction_amount)); // CPU Avail
// 		tbl.appendChild(newRow);
// 	}
// 	tdoc.appendChild(tbl);

// 	tdoc.DataTable();
// }


function modifyCapRequestEntry() {
	row_item = tableEventProcessor();
	update_json = processFormProcessor();
	console.log(row_item);
	console.log(update_json);
	input_json = {
		'original_data': row_item,
		'update_data': update_json,
	};
	axios.post(
		'/modify_request', json = input_json
	).then((response) => {
		status_out = response.data;
		console.log(status_out);
		popSnackbar(row_item['fqdn'], "updated");
		location.reload();
	})
		.catch((error) => {
			console.log('error ' + error);
		});
}
// Deprecated function to submit a selected checkbox
function uploadEventProcessor() {

}
function tableEventProcessor() {
	event.preventDefault();
	console.log("Processing table");
	var grid = document.getElementById("expense_table");
	var checkBoxes = grid.getElementsByTagName("INPUT");
	var sum = 0;
	// // Foobar1	ACT - 43	foobar.nskope.com	4	10	2	sjc1
	for (var i = 0; i < checkBoxes.length; i++) {
		if (checkBoxes[i].checked) {
			var row = checkBoxes[i].parentNode.parentNode;
			console.log(row.cells[5].innerHTML);
			sum = sum + parseInt(row.cells[5].innerHTML);
		}
	}
	var sumDoc = document.getElementById("sum_doc");
	sumDoc.type = "text";
	sumDoc.value = sum;
}

