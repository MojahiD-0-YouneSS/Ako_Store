function dropdown() {
  var dropdownHover = document.getElementsByClassName("dropdown-hover");
  var dropdownCard = document.getElementsByClassName("dropdown-card");
  for (var i = 0; i < dropdownHover.length; i++) {
    dropdownHover[i].addEventListener("mouseover", function () {
      var dropdown = this.querySelector(".dropdown-card");
      if (dropdown) {
        dropdown.style.display = "block";
      }
    });

    dropdownHover[i].addEventListener("mouseout", function () {
      var dropdown = this.querySelector(".dropdown-card");
      if (dropdown) {
        dropdown.style.display = "none";
      }
    });
  }
}

function setAction(action) {
  document.getElementById("action").value = action;
}

function input_size_quantity() {
  const sizeForm = document.getElementById("size-form");
  const sizeSelect = document.getElementById("id_size");
  const quantityInput = document.getElementById("id_quantity_size");
  const sizeQuantityInput = document.getElementById("size_quantity_input");

  const sizeQuantityDict = {};

  document.getElementById("add-size").addEventListener("click", function () {
    const selectedSize = sizeSelect.value;
    const quantity = quantityInput.value;

    if (selectedSize && quantity) {
      sizeQuantityDict[selectedSize] = parseInt(quantity);
      console.log(sizeQuantityDict)
      sizeQuantityInput.value = JSON.stringify(sizeQuantityDict);
      
      renderSizeQuantityList();
    }
  });
}
function renderSizeQuantityList() {
  const listContainer = document.getElementById("size-quantity-list");
  listContainer.innerHTML = "";
  for (const [size, quantity] of Object.entries(sizeQuantityDict)) {
    const listItem = document.createElement("li");
    listItem.textContent = `Size: ${size}, Quantity: ${quantity}`;
    listContainer.appendChild(listItem);
  }
}
