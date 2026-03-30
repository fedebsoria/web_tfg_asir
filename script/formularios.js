document.addEventListener("DOMContentLoaded", () => {
  const logoutButton = document.getElementById("logout-button");
  const saveSaleForm = document.getElementById("save-sale-form");
  const newOrderButton = document.getElementById("new-order-button");

  const detailBox = document.querySelector(".detail-box");
  const detailText = detailBox?.querySelector("p");
  const detailLinesContainer = detailBox?.querySelector(".detail-lines");
  const orderTotal = detailBox?.querySelector(".order-total span:last-child");

  const productFields = [
    {
      product: document.getElementById("producto-1"),
      value: document.getElementById("valor-producto-1"),
      quantity: document.getElementById("cantidad-1"),
    },
    {
      product: document.getElementById("producto-2"),
      value: document.getElementById("valor-producto-2"),
      quantity: document.getElementById("cantidad-2"),
    },
    {
      product: document.getElementById("producto-3"),
      value: document.getElementById("valor-producto-3"),
      quantity: document.getElementById("cantidad-3"),
    }
  ];

  const commentsField = document.getElementById("comentarios");

  if (logoutButton) {
    logoutButton.addEventListener("click", () => {
      const confirmLogout = confirm("¿Deseas cerrar sesión?");
      if (confirmLogout) {
        window.location.href = "index.html";
      }
    });
  }

  function formatCurrency(amount) {
    return `$${amount.toFixed(2)}`;
  }

  function resetOrderDetail() {
    if (detailText) {
      detailText.textContent = "Aquí aparecerá el detalle del pedido guardado.";
    }

    if (detailLinesContainer) {
      detailLinesContainer.innerHTML = `
        <div class="detail-line">
          <span>Producto 1</span>
          <span>0 x 0</span>
        </div>
        <div class="detail-line">
          <span>Producto 2</span>
          <span>0 x 0</span>
        </div>
        <div class="detail-line">
          <span>Producto 3</span>
          <span>0 x 0</span>
        </div>
      `;
    }

    if (orderTotal) {
      orderTotal.textContent = "$0.00";
    }
  }

  function buildOrderDetail() {
    let total = 0;
    let linesHTML = "";
    let hasProducts = false;

    productFields.forEach((field, index) => {
      const productName = field.product.value;
      const productLabel = field.product.options[field.product.selectedIndex]?.text || `Producto ${index + 1}`;
      const value = parseFloat(field.value.value);
      const quantity = parseInt(field.quantity.value, 10);

      const hasAnyValue =
        productName !== "" ||
        field.value.value.trim() !== "" ||
        field.quantity.value.trim() !== "";

      if (!hasAnyValue) {
        return;
      }

      if (!productName || isNaN(value) || isNaN(quantity) || value < 0 || quantity < 1) {
        throw new Error(`Revisa los datos de la línea ${index + 1}.`);
      }

      const lineTotal = value * quantity;
      total += lineTotal;
      hasProducts = true;

      linesHTML += `
        <div class="detail-line">
          <span>${productLabel}</span>
          <span>${quantity} x ${formatCurrency(value)} = ${formatCurrency(lineTotal)}</span>
        </div>
      `;
    });

    if (!hasProducts) {
      throw new Error("Debes introducir al menos un producto válido.");
    }

    if (detailText) {
      detailText.textContent = "Pedido guardado correctamente.";
    }

    if (detailLinesContainer) {
      detailLinesContainer.innerHTML = linesHTML;
    }

    if (orderTotal) {
      orderTotal.textContent = formatCurrency(total);
    }
  }

  if (saveSaleForm) {
    saveSaleForm.addEventListener("submit", (event) => {
      event.preventDefault();

      try {
        buildOrderDetail();

        if (commentsField && commentsField.value.trim() !== "") {
          console.log("Comentario:", commentsField.value.trim());
        }

        alert("Venta guardada correctamente.");
      } catch (error) {
        alert(error.message);
      }
    });
  }

  if (newOrderButton) {
    newOrderButton.addEventListener("click", () => {
      if (saveSaleForm) {
        saveSaleForm.reset();
      }

      resetOrderDetail();
    });
  }

  resetOrderDetail();
});