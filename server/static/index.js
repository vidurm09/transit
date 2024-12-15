const apiUrl = "https://your-api-endpoint.com"; // Replace with your actual API endpoint

function renderData(dataList) {
    const busList = document.querySelector(".bus-list");
    busList.innerHTML = "";

    dataList.forEach(stop => {
        var nextArrival;
        if (stop.estimatedArrivalTimes.length > 1) {
            nextArrival = getStringFromTimestamp(stop.estimatedArrivalTimes[1]);
        } else {
            nextArrival = "none"
        }
        const listItem = document.createElement("li");
        const busInfo = document.createElement("div");
        busInfo.classList.add("bus-info");

        
        const upcomingArrivalTime = stop.estimatedArrivalTimes[0];
        // Parse the arrival time using appropriate methods
        const parsedArrivalTime = new Date(upcomingArrivalTime);
        const minutesUntilArrival = Math.floor((parsedArrivalTime - new Date()) / 60000);
        const busDetails = document.createElement("div");
        busDetails.classList.add("bus-details");
        // Display bus line, minutes until arrival, and stop point name
        busDetails.innerHTML = `
            <h2>${stop.busLine} <span class="minsUntilArrival">(${minutesUntilArrival > 0 ? minutesUntilArrival : 0} min) ${stop.destinationName}</span></h2>
            <small>${stop.stopPointName}</small>
        `;

        const arrivalTimes = document.createElement("div");
        arrivalTimes.classList.add("arrival-times");
        arrivalTimes.innerHTML = `
            <p>Arriving: ${getStringFromTimestamp(stop.estimatedArrivalTimes[0])}</p>
            <p>Next: ${nextArrival}</p>
        `;

        busInfo.appendChild(busDetails);
        busInfo.appendChild(arrivalTimes);
        listItem.appendChild(busInfo);
        busList.appendChild(listItem);
    });
}

function updateData() {
	const currentUrl = `${window.location.origin}${window.location.pathname}`;
	const fullUrl = `${currentUrl}/updateData`;
	fetch(fullUrl)
        .then(response => response.json())
        .then(data => {
            renderData(data);
        })
        .catch(error => {
            console.error("Error fetching data: ", error);
        });

}

function getStringFromTimestamp(timestamp) {
    return getStringFromDate(new Date(timestamp))
}

function getStringFromDate(date) {
    const hours = date.getHours();
    const minutes = date.getMinutes().toString().padStart(2, '0'); // Add leading zero if needed
    const ampm = hours >= 12 ? 'PM' : 'AM';

    // Adjust hours for 12-hour format (if desired)
    const adjustedHours = hours % 12 || 12; // Show 12 for midnight

    // Format the time string
    return `${adjustedHours}:${minutes} ${ampm}`;
}

const fetchData = setInterval(updateData, 10000);
updateData();
