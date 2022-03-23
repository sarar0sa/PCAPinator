// js-function to fetch data. Mostly here as an annoying middle-hand to refresh the page after a request 
// as flask's send_file() can't handle that. Need to refresh page to show successfull-feedback to user. 

function fetch_data(event) {
    event.preventDefault();
    showSpinner();
    var pcap_id = document.getElementById("pcap_id");
    var device_name = document.getElementById("device_name");
    var session_id = document.getElementById("session_id");
    var search_time = document.getElementById("search_time");

    var parameters = {
        pcap_id: pcap_id.value,
        device_name: device_name.value,
        session_id: session_id.value,
        search_time: search_time.value
    };

    fetch("/", {
        method: "POST",
        body: JSON.stringify(parameters),
        cache: "no-cache",
        headers: {
            "content-type": "application/json",
        }
    })
        .then(response => {
            console.log(response)
            if(response.status !== 200){
                throw new Error("Error")
            }
            return response.blob()
        }).then(blob => {
            do_download(blob, parameters);
        }).then(() => {
            refresh();
        })
        .catch(error => {
            console.log(error)
            refresh();
        });
}

// Download the content by creating a link
function do_download(blob, parameters) {
    console.log('Downloading file');
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = `${parameters.pcap_id}.pcap`;
    document.body.appendChild(a);
    a.click();
    console.log("URL: ", url);
    window.URL.revokeObjectURL(url);
}

// Show downloading-button wiht spinner
function showSpinner() {
    document.getElementById("submit").style.display = 'none';
    document.getElementById("loading-btn").style.visibility = 'visible';
} 

// Refreshes the page
function refresh() {    
    setTimeout(function () {
        window.location.reload()
    }, 100);
}