function selectImages() {
  // JavaScript for product Images
  const images = document.querySelectorAll(".selectable-image");
  images.forEach((image) => {
    image.addEventListener("click", () => {
      image.classList.toggle("selected");
    });
  });
}

// For side panel
function openPanel() {
  const panel = document.getElementById("panel");
  if (panel) {
    panel.classList.toggle("show");
  } else {
    console.error("Element with ID 'panel' not found.");
  }
}


function closePanel() {
  const panel = document.getElementById("panel");
  if (panel) {
    panel.style.left = panel.style.left === "0px" ? "-250px" : "0px";
    document.getElementById("main").classList.remove("panel-open");
  } else {
    console.error("Element with ID 'panel' not found.");
  }
}

// Toggle image visibility for the first container
function toggleImages1() {
  const lgo1 = document.getElementById("LGO1");
  const lgo2 = document.getElementById("LGO2");

  if (lgo1 && lgo2) {
    if (lgo1.style.display === "block") {
      lgo1.style.display = "none";
      lgo2.style.display = "block";
    } else {
      lgo1.style.display = "block";
      lgo2.style.display = "none";
    }
  }
}

// Check first container visibility and toggle images
function checkContainerVisibility1() {
  const container1 = document.getElementById("pic1");
  if (container1 && window.getComputedStyle(container1).display === "block") {
    toggleImages1();
  }
}

// Toggle image visibility for the second container
function toggleImages2() {
  const lgo3 = document.getElementById("LGO3");
  const lgo4 = document.getElementById("LGO4");

  if (lgo3 && lgo4) {
    if (lgo3.style.display === "block") {
      lgo3.style.display = "none";
      lgo4.style.display = "block";
    } else {
      lgo3.style.display = "block";
      lgo4.style.display = "none";
    }
  }
}

// Check second container visibility and toggle images
function checkContainerVisibility2() {
  const container2 = document.getElementById("buttons2");
  if (container2 && window.getComputedStyle(container2).display === "block") {
    toggleImages2();
  }
}

// Slideshow functionality

function showSlides(n) {
  const slides = document.getElementsByClassName("slide");
  const dots = document.getElementsByClassName("dot");
  if (n >= slides.length) {
    slideIndex = 0;
  }
  if (n < 0) {
    slideIndex = slides.length - 1;
  }
  for (let i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (let i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  if (slides[slideIndex]) {
    slides[slideIndex].style.display = "block";
  }
  if (dots[slideIndex]) {
    dots[slideIndex].className += " active";
  }
}

function changeSlide(n) {
  showSlides((slideIndex += n));
}

function currentSlide(n) {
  showSlides((slideIndex = n));
}

// Auto change slides every 2 seconds
setInterval(function () {
  changeSlide(1);
}, 2000);

// Load headline content
function headline(url) {
  const selfAdds = document.getElementById("self_adds");

  if (!selfAdds) {
    console.error("Element with ID 'self_adds' not found.");
    return;
  }

  console.log("Fetching content from URL:", url); // Debugging log

  fetch(url)
    .then((response) => {
      console.log("Fetch response received"); // Debugging log
      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }
      return response.text();
    })
    .then((html) => {
      console.log("HTML content fetched successfully"); // Debugging log
      selfAdds.innerHTML = html;
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      );
    });
}

// Social icons hover effect
function socialIcons() {
  const container = document.getElementById("button_container");
  const socialIcons = document.querySelector(".social-icons");

  container.addEventListener("mouseenter", () => {
    socialIcons.classList.add("active");
  });

  container.addEventListener("mouseleave", () => {
    socialIcons.classList.remove("active");
  });
}

// Replace form action based on action type
function replace_action(actionType, product_id, color = null) {
  console.log("replace_action called");
  console.log("actionType:", actionType);
  console.log("product_id:", product_id);
  console.log("color:", color);
  const form = document.getElementById("cartForm");
  const baseUrl = "/cart";
  if (form) {
    if (actionType === "add_to_cart") {
      form.action = `${baseUrl}/add/${product_id}/`;
    } else if (actionType === "update_cart") {
      form.action = `${baseUrl}/update/${product_id}/${color}/`;
    } else if (actionType === "add_to_temp_cart") {
      form.action = `${baseUrl}/add_to_temp_cart/${product_id}/`;
    }
    form.submit();
  } else {
    console.error("Element with ID 'cartForm' not found.");
  }
}

function ALL_wearheadline(url) {
  const selfAdds = document.getElementById("lib-wear");

  if (!selfAdds) {
    console.error("Element with ID 'lib-wear' not found.");
    return;
  }

  console.log("Fetching content from URL:", url); // Debugging log

  fetch(url)
    .then((response) => {
      console.log("response :", response);
      console.log("Fetch response received"); // Debugging log
      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }
      return response.text();
    })
    .then((html) => {
      console.log("HTML content fetched successfully"); // Debugging log
      selfAdds.innerHTML = html;
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      );
    });
}

let topCurrentIndex = 0;
let downCurrentIndex = 0;
let feetCurrentIndex = 0;

function slide_TOP(index) {
  const topContainers = document.querySelectorAll(".Top_headline_container");
  topContainers.forEach((container, i) => {
    container.style.display = i === index ? "block" : "none";
  });
}

function arrow_left_TOP() {
  const topContainers = document.querySelectorAll(".Top_headline_container");
  topCurrentIndex =
    (topCurrentIndex - 1 + topContainers.length) % topContainers.length;
  slide_TOP(topCurrentIndex);
}

function arrow_right_TOP() {
  const topContainers = document.querySelectorAll(".Top_headline_container");
  topCurrentIndex = (topCurrentIndex + 1) % topContainers.length;
  slide_TOP(topCurrentIndex);
}

function slide_Down(index) {
  const downContainers = document.querySelectorAll(".Down_headline_container");
  downContainers.forEach((container, i) => {
    container.style.display = i === index ? "block" : "none";
  });
}

function arrow_left_Down() {
  const downContainers = document.querySelectorAll(".Down_headline_container");
  downCurrentIndex =
    (downCurrentIndex - 1 + downContainers.length) % downContainers.length;
  slide_Down(downCurrentIndex);
}

function arrow_right_Down() {
  const downContainers = document.querySelectorAll(".Down_headline_container");
  downCurrentIndex = (downCurrentIndex + 1) % downContainers.length;
  slide_Down(downCurrentIndex);
}

function slide_Feet(index) {
  const feetContainers = document.querySelectorAll(".Feet_headline_container");
  feetContainers.forEach((container, i) => {
    container.style.display = i === index ? "block" : "none";
  });
}

function arrow_left_Feet() {
  const feetContainers = document.querySelectorAll(".Feet_headline_container");
  feetCurrentIndex =
    (feetCurrentIndex - 1 + feetContainers.length) % feetContainers.length;
  slide_Feet(feetCurrentIndex);
}

function arrow_right_Feet() {
  const feetContainers = document.querySelectorAll(".Feet_headline_container");
  feetCurrentIndex = (feetCurrentIndex + 1) % feetContainers.length;
  slide_Feet(feetCurrentIndex);
}

document.addEventListener("DOMContentLoaded", function () {
  slide_TOP(topCurrentIndex);
  slide_Down(downCurrentIndex);
  slide_Feet(feetCurrentIndex);
});

function outfit_selector(url_txt, usr) {
  const topwarerefContainer = document.querySelector(".Top_headline_container");
  const legwarerefContainer = document.querySelector(
    ".Down_headline_container"
  );
  const feetwarerefContainer = document.querySelector(
    ".Feet_headline_container"
  );

  if (!topwarerefContainer || !legwarerefContainer || !feetwarerefContainer) {
    console.error("One or more containers not found.");
    return;
  }

  const topwarerefSpan = topwarerefContainer.querySelector("span");
  const legwarerefSpan = legwarerefContainer.querySelector("span");
  const feetwarerefSpan = feetwarerefContainer.querySelector("span");

  if (!topwarerefSpan || !legwarerefSpan || !feetwarerefSpan) {
    console.error("One or more reference spans not found.");
    return;
  }

  const topwareref = topwarerefSpan.textContent.trim();
  const legwareref = legwarerefSpan.textContent.trim();
  const feetwareref = feetwarerefSpan.textContent.trim();

  const url = `${url_txt}${encodeURIComponent(topwareref)}/${encodeURIComponent(
    legwareref
  )}/${encodeURIComponent(feetwareref)}/${encodeURIComponent(usr)}`;

  fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }
      return response.json();
    })
    .then((data) => {
      console.log("Response from outfit_selector function:", data);
      // Handle the response data if needed
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
}

