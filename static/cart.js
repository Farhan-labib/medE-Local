document.addEventListener('DOMContentLoaded', function () {
  updateCartBadge();
});

function updateCartBadge() {
  var cart = JSON.parse(localStorage.getItem('cart')) || {};
  var cartLength = Object.keys(cart).length;
  // console.log(cartLength);
  // Update the content of the span with the cart length
  var cartBadgeSpan = document.querySelector('.btn-badge');
  if (cartBadgeSpan) {
    cartBadgeSpan.textContent = cartLength;
  }
}


async function AddtoCart(id, quantity = 1, doSomething = null, button = null) {
  var cart = JSON.parse(localStorage.getItem('cart')) || {};

  try {
    // Make an asynchronous API call to get the product data using the product ID
    const response = await fetch(`/get_product_info/${id}`);
    if (response.ok) {
      const productData = await response.json();

      if (cart[id] === undefined) {
        // console.log("Added to cart:", id);
        
        cart[id] = parseInt(quantity);
      } else if (cart[id] !== undefined && doSomething === null) {
        cart[id] += quantity;
      } else if (doSomething === "increment") {
        cart[id] += 1;
      } else if (doSomething === "decrement" && cart[id] > 1) {
        cart[id] -= 1;
      } else if (doSomething === "replace") {
        cart[id] = parseInt(quantity);
      }

      // console.log(cart);
      localStorage.setItem('cart', JSON.stringify(cart));
      await totalBill();

      // Update the quantity element directly if a button is provided
      if (button) {
        const quantityElement = button.parentElement.querySelector(".quantity-value");
        if (quantityElement) {
          quantityElement.textContent = cart[id];
        }
      }

      // Update the total price for this item in the cart
      const totalPriceElement = document.getElementById(`totalPrice-${id}`);
      if (totalPriceElement) {
        totalPriceElement.textContent = `৳` + `${(cart[id] * productData.discounted_price).toFixed(2)}`;
      }
    } else {
      console.log("Response Error");
    }
  } catch (error) {
    console.error('Error:', error);
  }
  updateCartBadge();
}


////Didn't used in this file but mmight come useful later

async function getProductData(productId) {
  try {
    const response = await fetch(`/get_product_info/${productId}/`);
    if (response.ok) {
      const productData = await response.json();
      return productData;
    } else {
      console.error('Error fetching product data');
      return null;
    }
  } catch (error) {
    console.error('Error:', error);
    return null;
  }
}



async function removeFromCart(productId) {
  var cart = JSON.parse(localStorage.getItem('cart')) || {};

  // Check if the productId is in the cart
  if (cart.hasOwnProperty(productId)) {
    // Remove the product from the cart
    delete cart[productId];
    // Update the cart in localStorage
    localStorage.setItem('cart', JSON.stringify(cart));

    // Call totalBill to update and display the new total
    await totalBill();

    // Hide the corresponding cartbox div
    let cartboxId = `cartbox-${productId}`;
    let cartboxElement = document.getElementById(cartboxId);
    if (cartboxElement) {
      cartboxElement.style.display = 'none';
    }
  } else {
    // console.log('Product not found in the cart.');
  }
  updateCartBadge();
}





function ClearCart() {
  console.log('clearing cart');
  localStorage.removeItem('cart');
  cart = {}
  // console.log(cart)
  updateCartBadge();
}

var totalValue = 0.0; // Initialize total value to 0.0

document.getElementById("cart-btn").addEventListener("click", async function () {
  totalValue = await totalBill();
  var cart = JSON.parse(localStorage.getItem('cart'));
  var resultsDiv = $('#cart-container');

  // Clear the existing content
  resultsDiv.empty();

  // Get the sorted array of product IDs
  var sortedProductIds = Object.keys(cart).sort(function (a, b) {
    return a - b;
  });

  // Loop through the sorted product IDs and create fetch requests
  for (const p_id of sortedProductIds) {
    try {
      // Fetch the product information for the current p_id
      const response = await fetch(`/get_product_info/${p_id}/`);
      if (response.ok) {
        const productData = await response.json();
        // console.log("Product Data:", productData);
        var productPrice = parseFloat(productData.discounted_price).toFixed(2);

        if (Object.keys(productData).length > 0 && "p_name" in productData) {
          // Display the product name
          // <a href="{%url 'prod' p_name=product.p_name %}"></a>
          resultsDiv.append(`
                  <div class="cartbox" id="cartbox-${p_id}">
                            
                  <img src="../../media/${productData["p_image"]}" alt="">
                  <div class="cart-content-${p_id}">
                  <h3><a style="color:black;" href="/product/${productData["p_name"]}/">${productData["p_name"]}</a></h3>
                      <div style="display: grid; grid-template-columns: 0.5fr 1fr; gap: 20px;">
                      <span class="quantity">
                          <button class="quantity-button decrement" style="display: inline; white-space: nowrap;"
                              onclick="AddtoCart(${productData["p_id"]},${cart[productData["p_id"]]}, 'decrement', this)">-</button>
                          <span class="quantity-value" id="quantity-${p_id}">${cart[productData["p_id"]]}</span>  
                          <button class="quantity-button increment" style="display: inline; white-space: nowrap;"
                              onclick="AddtoCart(${productData["p_id"]},${cart[productData["p_id"]]}, 'increment', this)">+</button>
                      </span>
                      <span id="totalPrice-${p_id}">৳${(cart[productData["p_id"]] * productData['discounted_price']).toFixed(2)}</h3>
                      </div>
                  </div>
                  <button class="cart-trash" onclick="removeFromCart(${productData["p_id"]})">
                      <ion-icon name="trash"></ion-icon>
                  </button>
              </div>`

            // The line below to go right before where the div closes. Commented out for convenience 

          );
        } else {
          resultsDiv.append('<p>No product name found.</p>');
        }
      } else {
        resultsDiv.append('<p>No results found.</p>');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }
});

async function totalBill() {
  var cart = JSON.parse(localStorage.getItem('cart')) || {};
  // Get the sorted array of product IDs
  var sortedProductIds = Object.keys(cart).sort(function (a, b) {
    return a - b;
  });

  total = 0.0;
  try {
    for (const p_id of sortedProductIds) {
      const response = await fetch(`/get_product_info/${p_id}/`);
      if (response.ok) {
        const productData = await response.json();
        total += parseFloat((cart[productData["p_id"]] * productData['discounted_price'] ).toFixed(2));
      } else {
        console.log("Response Error")
      }
    }
    // console.log(total) 
    const totalElement = document.querySelector('.total');
    if (totalElement) {
      totalElement.textContent = `Total:` + total.toFixed(2);
    }


  } catch (error) { // Define the error variable here
    console.error('Error:', error);
  }
  updateCartBadge();

}


document.getElementById('checkout-button').addEventListener('click', function () {
  var cart = JSON.parse(localStorage.getItem('cart')) || {};

  // Get the CSRF token
  var csrftoken = getCookie('csrftoken'); // You'll need a function to get the CSRF token

  // Define the URL and request options
  var url = 'checkout/';
  var requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken, // Include the CSRF token in the request header
    },
    body: JSON.stringify(cart),
  };

  // Send the cart data to the server using fetch
  var url = '/checkout/';
  fetch(url, requestOptions)
    .then(function (response) {
      if (response.status === 200) {
        // console.log('Checkout was successful');
        window.location.href = '/order_confirm/';
      }
    })

});

// Function to get the CSRF token from the cookie
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


