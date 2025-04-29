const cartStyles = `
.cart-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f9f9f9;
  padding: 12px;
  border-radius: 10px;
  margin-bottom: 10px;
  box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.1);
}
.cart-item img {
  width: 70px;
  height: auto;
  margin-right: 15px;
}
.cart-content {
  flex: 1;
}
.cart-content h3 a {
  font-size: 16px;
  color: #333;
  text-decoration: none;
  font-weight: bold;
}
.cart-content .quantity-display {
  font-size: 14px;
  color: #555;
}
.cart-content .quantity-controls {
  display: flex;
  gap: 10px;
}
.cart-content .quantity-button {
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.cart-content .quantity-button:hover {
  background-color: #0056b3;
}
.cart-content .price-info {
  font-size: 16px;
  font-weight: bold;
}
.cart-trash {
  background: none;
  border: none;
  color: red;
  cursor: pointer;
}
.cart-trash ion-icon {
  font-size: 18px;
}
.cart-trash:hover {
  color: darkred;
}
.cart-container {
  margin-top: 20px;
}
.total {
  font-size: 18px;
  font-weight: bold;
  margin-top: 20px;
  text-align: right;
}
`;

const styleSheet = document.createElement("style");
styleSheet.type = "text/css";
styleSheet.innerText = cartStyles;
document.head.appendChild(styleSheet);

document.addEventListener('DOMContentLoaded', function() {
  updateCartBadge();
});

function updateCartBadge() {
  const cart = JSON.parse(localStorage.getItem('cart')) || {};
  const cartLength = Object.keys(cart).length;
  const cartBadgeSpan = document.querySelector('.btn-badge');
  if (cartBadgeSpan) {
    cartBadgeSpan.textContent = cartLength;
  }
}

async function AddtoCart(id, quantity = 1, doSomething = null, button = null) {
  const cart = JSON.parse(localStorage.getItem('cart')) || {};
  const packagingSelect = document.getElementById('packaging');
  const packaging = packagingSelect ? packagingSelect.value : 'Piece';
  
  try {
    const response = await fetch(`/get_product_info/${id}`);
    if (response.ok) {
      const productData = await response.json();
      
      const medPerStrip = Math.max(1, productData.medPerStrip || 1);
      const stripPerBox = Math.max(1, productData.stripPerBox || 1);
      
      if (cart[id] === undefined || doSomething === "replace") {
        cart[id] = {
          packaging: packaging,
          quantity: quantity,
          price: productData.discounted_price,
          medPerStrip: medPerStrip,
          stripPerBox: stripPerBox,
          name: productData.p_name,
          image: productData.p_image
        };
      } 
      else if (doSomething === "increment" || doSomething === "decrement") {
        if (doSomething === "increment") {
          cart[id].quantity += 1;
        } else {
          if (cart[id].quantity > 1) {
            cart[id].quantity -= 1;
          } else {
            delete cart[id];
          }
        }
      }
      else {
        cart[id].quantity += quantity;
      }
      
      localStorage.setItem('cart', JSON.stringify(cart));
      await updateCartDisplay();
      
      if (button && doSomething === null) {
        const quantityElement = button.parentElement.querySelector(".quantity-value");
        if (quantityElement) {
          quantityElement.textContent = quantity.toString().padStart(2, '0');
        }
      }
    }
  } catch (error) {
    /* Error handling */
  }
  
  updateCartBadge();
}

async function removeFromCart(productId) {
  const cart = JSON.parse(localStorage.getItem('cart')) || {};
  
  if (cart[productId]) {
    delete cart[productId];
    localStorage.setItem('cart', JSON.stringify(cart));
    await updateCartDisplay();
    
    const itemElement = document.getElementById(`cart-item-${productId}`);
    if (itemElement) {
      itemElement.remove();
    }
  }
  
  updateCartBadge();
}

async function updateCartDisplay() {
  const cart = JSON.parse(localStorage.getItem('cart')) || {};
  const resultsDiv = document.getElementById('cart-container');
  if (!resultsDiv) return;
  
  resultsDiv.innerHTML = '';
  
  let total = 0;
  for (const [p_id, item] of Object.entries(cart)) {
    let totalPieces = item.quantity;
    if (item.packaging === 'Pack') {
      totalPieces = item.quantity * item.medPerStrip;
    } else if (item.packaging === 'Box') {
      totalPieces = item.quantity * item.medPerStrip * item.stripPerBox;
    }
    
    const itemTotal = totalPieces * item.price;
    total += itemTotal;
    
    let displayText = '';
    if (item.packaging === 'Piece') {
      displayText = `${item.quantity} piece${item.quantity !== 1 ? 's' : ''}`;
    } else if (item.packaging === 'Pack') {
      displayText = `${item.quantity} pack${item.quantity !== 1 ? 's' : ''} (${item.medPerStrip} pieces per pack)`;
    } else if (item.packaging === 'Box') {
      displayText = `${item.quantity} box${item.quantity !== 1 ? 'es' : ''} (${item.stripPerBox} packs per box, ${item.medPerStrip} pieces per pack)`;
    }
    
    const itemElement = document.createElement('div');
    itemElement.className = 'cart-item';
    itemElement.id = `cart-item-${p_id}`;
    itemElement.innerHTML = `
      <img src="../../media/${item.image}" alt="${item.name}">
      <div class="cart-content">
        <h3><a href="">${item.name}</a></h3>
        <div class="quantity-display">
          <span class="units">${displayText}</span>
          <small>(Total: ${totalPieces} pieces)</small>
        </div>
        <div class="quantity-controls">
          <button class="quantity-button decrement" onclick="AddtoCart('${p_id}',1,'decrement',this)">-</button>
          <button class="quantity-button increment" onclick="AddtoCart('${p_id}',1,'increment',this)">+</button>
        </div>
        <div class="price-info">
          <span>৳${itemTotal.toFixed(2)}</span>
        </div>
      </div>
      <button class="cart-trash" onclick="removeFromCart('${p_id}')">
        <ion-icon name="trash"></ion-icon>
      </button>
    `;
    
    resultsDiv.appendChild(itemElement);
  }
  
  const totalElement = document.querySelector('.total');
  if (totalElement) {
    totalElement.textContent = `Total: ৳${total.toFixed(2)}`;
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
  const cartBtn = document.getElementById("cart-btn");
  if (cartBtn) {
    cartBtn.addEventListener("click", updateCartDisplay);
  }
  
  const checkoutButton = document.getElementById('checkout-button');
  if (checkoutButton) {
    checkoutButton.addEventListener("click", async function() {
      const cart = JSON.parse(localStorage.getItem('cart')) || {};
      
      if (Object.keys(cart).length === 0) {
        alert("Your cart is empty!");
        return;
      }
      try {
        const csrftoken = getCookie('csrftoken');
        const response = await fetch('/checkout/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
          },
          body: JSON.stringify(cart),
        });
        if (response.ok) {
          window.location.href = '/order_confirm/';
        } else {
          alert('Checkout failed. Please try again.');
        }
      } catch (error) {
        alert('An error occurred during checkout.');
      }
    });
  }
});