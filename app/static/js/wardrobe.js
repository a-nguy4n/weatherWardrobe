  function filterClothingItem() {
      // TODO: Add logic
      console.log("Clothes Filter");
    }

    function addClothingItem() {
      document.getElementById("addWindow").style.display = "block";
      console.log("Opening Add Clothing Item Form");
    }

    function removeClothingItem() {
      document.getElementById("removeWindow").style.display = "block";
      console.log("Clothing Item Removed");
    }

    function updateClothingItem() {
      document.getElementById("updateWindow").style.display = "block";
      console.log("Clothing Item Updated");
    }

    function closeForm(){
      document.getElementById("addWindow").style.display = "none"; 
      document.getElementById("removeWindow").style.display = "none"; 
      document.getElementById("updateWindow").style.display = "none"; 
    }

    //------  ADD ITEM FUNCTIONALITY------ 

    async function getUsername() {
      let response = await fetch("/api/user/me", { credentials: "include"});
      let data = await response.json();
      return data.username;
    }

    document.querySelector(".addItemForm").addEventListener("submit", async function (event) {
    event.preventDefault(); 

    let itemName = document.getElementById("clothingName").value.trim();
    let itemCategory = document.getElementById("itemCategory").value;
    let itemSize = document.getElementById("itemSize").value;
    let username = await getUsername();
      
  
    if(itemName.trim() === "" || itemCategory.trim() === "" || itemSize.trim() === "") {
      alert("Please fill out all fields.");
      return;
    }

    let formData = new FormData();
    formData.append("username", username);
    formData.append("name", itemName);
    formData.append("category", itemCategory);
    formData.append("size", itemSize);

    try {
      let response = await fetch("/api/wardrobe/add", {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      let data = await response.json();

      if (response.ok) {
        let card = document.createElement("div");
        card.classList.add("clothingCard");
        card.setAttribute("data-name", itemName.toLowerCase()); // for case sensitive 
        card.innerHTML = `
        <h3>${itemName}</h3>
        <p><strong>Category:</strong> ${itemCategory}</p>
        <p><strong>Size:</strong> ${itemSize}</p>
      `;   
        // <button class="removeCardButton" onclick="removeClothingCard(this)">Remove</button>

        document.getElementById("clothingDisplay").appendChild(card);

        closeForm();

        document.getElementById("clothingName").value = "";
        document.getElementById("itemCategory").value = "tops";
        document.getElementById("itemSize").value = "xxSmall";

        alert(data.message);
      }

      else {
        alert(`Error: ${data.error}`);
      }
    }

    catch (error) {
      console.error("Error:", error);
    }
  });

  // each card has remove
  // function removeClothingCard(button){
  //   button.parentElement.remove();
  // }


  // ------  REMOVE ITEM FUNCTIONALITY ------ 

  document.querySelector(".removeItemForm").addEventListener("submit", async function(event){
    event.preventDefault(); 

    let itemNameToRemove = document.getElementById("clothingNameRemove").value.trim().toLowerCase();

    console.log(itemNameToRemove);

    if (itemNameToRemove === "") {
      alert("Please enter a valid item name to remove.");
      return;
    }

    try {
      let response = await fetch(`/api/wardrobe/remove/${encodeURIComponent(itemNameToRemove)}`, {
        method: "DELETE",
        credentials: "include"
      });

      let data = await response.json();

      if (response.ok) {
        let clothingCards = document.querySelectorAll(".clothingCard");
        let itemFound = false;
    
        clothingCards.forEach(card => {
        let cardName = card.getAttribute("data-name");
        console.log(cardName);
          if(cardName === itemNameToRemove) {
            card.remove();
            itemFound = true;
          }
        });

        if(!itemFound){
          alert("Item not found.");
        }

        else {
          alert(data.message);
        }

      }

      else {
        alert(`Error: ${data.detail}`);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while trying to remove the item.");
    }    

    closeForm();
    document.getElementById("clothingNameRemove").value = "";
  });

  // ------  UPDATE ITEM FUNCTIONALITY ------ 
  document.querySelector(".updateItemForm").addEventListener("submit", async function(event){
    event.preventDefault();

    let currentNameInput = document.getElementById("currentItemName");
    let newNameInput = document.getElementById("newItemName");

    if (!currentNameInput || !newNameInput) {
        alert("Error: Form elements not found.");
        return;
    }

    let itemNameToUpdate = currentNameInput.value.trim().toLowerCase();
    let newItemName = newNameInput.value.trim();

    if (itemNameToUpdate === "" || newItemName === "") {
        alert("Please fill out both fields.");
        return;
    }

    let formData = new FormData();
    formData.append("old_name", itemNameToUpdate);
    formData.append("new_name", newItemName);

    try {
      let response = await fetch(`/api/wardrobe/update`, {
        method: "PUT",
        body: formData,
      });

      let data = await response.json();

      if(response.ok) {
        let clothingCards = document.querySelectorAll(".clothingCard");
        let itemFound = false;
    
        clothingCards.forEach(card => {
            let cardName = card.getAttribute("data-name");
            if (cardName === itemNameToUpdate) {
                card.querySelector("h3").innerText = newItemName;
                card.setAttribute("data-name", newItemName.toLowerCase());
                itemFound = true;
            }
        });
    
        if (!itemFound) {
            alert("Item not found.");
        } else {
            alert("Item successfully updated!");
        }
    
      }
      else {
        alert(`Error: ${data.detail}`);
      }
    }

    catch (error) {
      console.error("Error:", error);
      alert("An error occurred while trying to update the item.");
    }
    closeForm();
    currentNameInput.value = "";
    newNameInput.value = "";
  });


  async function fetchWardrobeItems() {
    try {
      let response = await fetch("/api/wardrobe", {
        credentials: "include"
      });
      let data = await response.json();

      if (response.ok) {
        let clothingDisplay = document.getElementById("clothingDisplay");
            clothingDisplay.innerHTML = ""; // Clear existing UI

            data.forEach(item => {
                let card = document.createElement("div");
                card.classList.add("clothingCard");
                card.setAttribute("data-name", item.name.toLowerCase());
                card.innerHTML = `
                    <h3>${item.name}</h3>
                    <p><strong>Category:</strong> ${item.category}</p>
                    <p><strong>Size:</strong> ${item.size}</p>
                `;
                clothingDisplay.appendChild(card);
            });
      }

      else {
        console.error("Error fetching wardrobe items:", data.detail);
      }
    }
    catch (error) {
      console.error("Error:", error);
    }
  }

  document.addEventListener("DOMContentLoaded", fetchWardrobeItems());
