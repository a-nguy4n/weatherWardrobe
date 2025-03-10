// function addDevice() {
//     // Need to add logic for adding device
//     console.log("Add device clicked");
//     }

//     function removeDevice() {
//     // Need to add logic for removing device 
//     console.log("Remove device clicked");
//     }

// document.addEventListener("DOMContentLoaded", async () => {
//     await loadDevices();
// });

// async function loadDevices() {
//     const devicesList = document.getElementById("devicesList");
//     devicesList.innerHTML = ""; // Clear existing devices

//     try {
//         const response = await fetch("/api/devices");
//         const devices = await response.json();

//         devices.forEach(device => {
//             const deviceDiv = document.createElement("div");
//             deviceDiv.className = "devicePlaceholder";
//             deviceDiv.innerHTML = `<p>${device.topic} (${device.status})</p>`;
//             devicesList.appendChild(deviceDiv);
//         });
//     } catch (error) {
//         console.error("Error loading devices:", error);
//     }
// }

// function openModal() {
//     document.getElementById("deviceModal").style.display = "block";
// }

// function closeModal() {
//     document.getElementById("deviceModal").style.display = "none";
// }

// document.getElementById("deviceForm").addEventListener("submit", async function(event) {
//     event.preventDefault();
    
//     const deviceId = document.getElementById("deviceId").value;
//     const deviceTopic = document.getElementById("deviceTopic").value;
//     const deviceStatus = document.getElementById("deviceStatus").value;

//     try {
//         const response = await fetch("/api/devices", {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify({ id: deviceId, topic: deviceTopic, status: deviceStatus })
//         });

//         if (response.ok) {
//             closeModal();
//             await loadDevices();
//         } else {
//             alert("Failed to register device");
//         }
//     } catch (error) {
//         console.error("Error adding device:", error);
//     }
// });

// document.addEventListener("DOMContentLoaded", () => {
//     fetchDevices();
// });

// async function fetchDevices() {
//     const username = "{{ user_data.email }}";  // Passed from Jinja2
//     const response = await fetch(`/api/devices/${username}`);
//     const data = await response.json();

//     const devicesContainer = document.getElementById("devicesContainer");
//     devicesContainer.innerHTML = "";  // Clear existing devices

//     if (data.devices) {
//         data.devices.forEach(device => {
//             const deviceDiv = document.createElement("div");
//             deviceDiv.classList.add("devicePlaceholder");
//             deviceDiv.innerHTML = `<p>${device.name}</p>`;
//             devicesContainer.appendChild(deviceDiv);
//         });
//     }
// }

// function showAddDeviceModal() {
//     document.getElementById("addDeviceModal").style.display = "block";
// }

// function closeAddDeviceModal() {
//     document.getElementById("addDeviceModal").style.display = "none";
// }

// async function addDevice() {
//     const deviceName = document.getElementById("deviceName").value;
//     if (!deviceName) return alert("Enter a device name");

//     const username = "{{ user_data.email }}";
    
//     const response = await fetch("/api/devices/add", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ username, device_name: deviceName })
//     });

//     if (response.ok) {
//         fetchDevices();  // Refresh list
//         closeAddDeviceModal();
//     } else {
//         alert("Failed to add device");
//     }
// }

// Show the modal when the "Add Device" button is clicked


// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("addDevice");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

var removeModal = document.getElementById("removeModal");

// Get the button that opens the modal
var removeBtn = document.getElementById("removeDevice");

// Get the <span> element that closes the modal
var removeSpan = document.getElementsByClassName("removeClose")[0];

// When the user clicks on the button, open the modal
removeBtn.onclick = function() {
  removeModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
removeSpan.onclick = function() {
  removeModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == removeModal) {
    removeModal.style.display = "none";
  }
}

async function removeDevice(deviceId, username) {
    try {
        const response = await fetch(`/profile/${username}/${deviceId}`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
        });

        if (response.ok) {
            const deviceElement = document.getElementById(deviceId);
            const deviceCardName = "deviceCard" + deviceId; 
            const deviceCard = document.getElementById(deviceCardName);

            if(deviceElement && deviceCard) {
                deviceElement.remove();
                deviceCard.remove();
            }

            else {
                console.warn(`Device with ID ${deviceId} not found in DOM.`)
            }
            alert("Device removed successfully!");
            
            closeRemoveModal();

        } else {
            const data = await response.json();
            alert("Error: " + data.error);
        }

    } catch (error) {
        console.error("Error deleting device: ", error);
    }
}

function closeRemoveModal() {
    document.getElementById("removeModal").style.display = "none";
}