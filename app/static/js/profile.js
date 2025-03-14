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