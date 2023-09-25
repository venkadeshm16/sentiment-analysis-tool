let menuicn = document.querySelector(".menuicn");
let nav = document.querySelector(".navcontainer");

menuicn.addEventListener("click", () => {
	nav.classList.toggle("navclose");
})

document.addEventListener("DOMContentLoaded", function () {
	updateCounts();
	var startDateValue;
	var endDateValue;
	function updateCounts() {
		var filterForm = document.getElementById('filter-form');
		// Add an event listener to the form submission
		filterForm.addEventListener('submit', function (event) {
			event.preventDefault(); // Prevent the form from submitting
	
			// Get references to the input fields
			var startDateInput = document.getElementById('start-date');
			var endDateInput = document.getElementById('end-date');
	
			// Access the values of the input fields
			startDateValue = startDateInput.value;
			endDateValue = endDateInput.value;
	
		});
		console.log('Start Dates:', startDateValue);
		console.log('End Dates:', endDateValue);
		
		fetch('/get_counts?start_date='+startDateValue+'&end_date='+endDateValue)
			.then(response => response.json())
			.then(data => {
				// Update the counts in the HTML
				document.getElementById("positive-count").textContent = data.positive;
				document.getElementById("negative-count").textContent = data.negative;
				document.getElementById("neutral-count").textContent = data.neutral;
				document.getElementById("total-count").textContent = data.total_comment;
			})
			.catch(error => {
				console.error('Error fetching counts:', error);
			});
	}

	// Optionally, you can update the counts periodically using setInterval
	setInterval(updateCounts, 5000); // Update every 5 seconds (adjust as needed)
});

document.addEventListener("DOMContentLoaded", function () {
    // Get a reference to the element with the id "redirect-element"
    var redirectElement = document.getElementById("logout");

    // Add a click event listener to the element
    redirectElement.addEventListener("click", function () {
        // Perform the redirection to the desired URL
        window.location.href = "/logout";
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Get a reference to the element with the id "redirect-element"
    var redirectElement = document.getElementById("positive");

    // Add a click event listener to the element
    redirectElement.addEventListener("click", function () {
        // Perform the redirection to the desired URL
        window.location.href = "/positive"
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Get a reference to the element with the id "redirect-element"
    var redirectElement = document.getElementById("negative");

    // Add a click event listener to the element
    redirectElement.addEventListener("click", function () {
        // Perform the redirection to the desired URL
        window.location.href = "/negative"
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Get a reference to the element with the id "redirect-element"
    var redirectElement = document.getElementById("neutral");

    // Add a click event listener to the element
    redirectElement.addEventListener("click", function () {
        // Perform the redirection to the desired URL
        window.location.href = "/neutral"
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Get a reference to the element with the id "redirect-element"
    var redirectElement = document.getElementById("home");

    // Add a click event listener to the element
    redirectElement.addEventListener("click", function () {
        // Perform the redirection to the desired URL
        window.location.href = "/home"
    });
});


document.addEventListener("DOMContentLoaded", function () {
	updateComments();
	var startDateValue;
	var endDateValue;
	function updateComments() {
		var filterForm = document.getElementById('filter-form');
		// Add an event listener to the form submission
		filterForm.addEventListener('submit', function (event) {
			event.preventDefault(); // Prevent the form from submitting

			// Get references to the input fields
			var startDateInput = document.getElementById('start-date');
			var endDateInput = document.getElementById('end-date');

			// Access the values of the input fields
			startDateValue = startDateInput.value;
			endDateValue = endDateInput.value;
		});
		$.ajax({
			url: '/get_comments?start_date='+startDateValue+'&end_date='+endDateValue, // Replace with your Flask endpoint URL
			type: 'GET',
			dataType: 'json',
			success: function(data) {
				// Clear existing content in the container
				$('#update-comments').empty();
				// Loop through the data and create new div elements
				data.forEach(function(comment) {
					var value = "green"; // Default value
					if (comment.sentiment_label === "Positive") {
						value = "green";
					} else if (comment.sentiment_label === "Negative") {
						value = "red";
					} else {
						value = "orange";
					}
	
					var newItem = '<div class="item1">' +
								  '<h3 class="t-op-nextlvl">' + comment.user + '</h3>' +
								  '<h3 class="t-op-nextlvl">' + comment.comment + '</h3>' +
								  '<h3 class="t-op-nextlvl label-tag" style="background-color: ' + value + ';">' + comment.sentiment_label + '</h3>' +
								  '</div>';
	
					// Append the new div element to the container
					$('#update-comments').append(newItem);
				});
			},
			error: function(error) {
				console.error('Error updating comments:', error);
			}
		});
	
	}

	setInterval(updateComments, 5000);
});

