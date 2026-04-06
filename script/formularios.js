document.addEventListener("DOMContentLoaded", () => {
  
    const logoutButton = document.getElementById("logout-button");
    const saveSaleForm = document.getElementById("save-sale-form");
    const newOrderButton = document.getElementById("new-order-button");
    const detailBox = document.querySelector(".detail-box");
    const detailText = detailBox?.querySelector("p");
    const detailLinesContainer = detailBox?.querySelector(".detail-lines");
    const orderTotal = detailBox?.querySelector(".order-total span:last-child");
    const commentsField = document.getElementById("comentarios");
    const usuarioIdField = document.getElementById("usuario_id");
    const userId = window.APP_USER_ID || 0;
    if (usuarioIdField) {
        usuarioIdField.value = userId;
    }
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

    function formatCurrency(amount) {
        return Number(amount).toFixed(2);
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
            orderTotal.textContent = "0.00";
        }
    }

    function buildOrderDetailFromResponse(lineas, totalPedido, pedidoId) {
        if (detailText) {
            detailText.textContent = `Pedido guardado correctamente. ID: ${pedidoId}`;
        }

        if (detailLinesContainer) {
            detailLinesContainer.innerHTML = lineas.map((linea) => `
                <div class="detail-line">
                    <span>${linea.producto}</span>
                    <span>${linea.cantidad} x ${formatCurrency(linea.precio_unitario)} = ${formatCurrency(linea.subtotal)}</span>
                </div>
            `).join("");
        }

        if (orderTotal) {
            orderTotal.textContent = formatCurrency(totalPedido);
        }
    }

    function rellenarPrecioDesdeSelect(selectElement, inputElement) {
        const selectedOption = selectElement.options[selectElement.selectedIndex];
        const precio = selectedOption?.dataset?.precio;

        if (precio && !inputElement.value.trim()) {
            inputElement.value = precio;
        }
    }

    productFields.forEach((field) => {
        if (field.product && field.value) {
            field.product.addEventListener("change", () => {
                rellenarPrecioDesdeSelect(field.product, field.value);
            });
        }
    });

    if (logoutButton) {
        logoutButton.addEventListener("click", () => {
            const confirmLogout = confirm("¿Deseas cerrar sesión?");
            if (confirmLogout) {
                window.location.href = "/logout";
            }
        });
    }

    if (saveSaleForm) {
        saveSaleForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            try {
                const productos = [];

                productFields.forEach((field, index) => {
                    const productoId = field.product.value.trim();
                    const productoLabel = field.product.options[field.product.selectedIndex]?.text || `Producto ${index + 1}`;
                    const valorTexto = field.value.value.trim();
                    const cantidadTexto = field.quantity.value.trim();

                    const hasAnyValue = productoId || valorTexto || cantidadTexto;

                    if (!hasAnyValue) {
                        return;
                    }

                    const precioUnitario = parseFloat(valorTexto);
                    const cantidad = parseInt(cantidadTexto, 10);

                    if (!productoId || Number.isNaN(precioUnitario) || Number.isNaN(cantidad) || precioUnitario < 0 || cantidad < 1) {
                        throw new Error(`Revisa los datos de la línea ${index + 1}: ${productoLabel}.`);
                    }

                    productos.push({
                        producto_id: parseInt(productoId, 10),
                        precio_unitario: precioUnitario,
                        cantidad: cantidad
                    });
                });

                if (!productos.length) {
                    throw new Error("Debes introducir al menos un producto válido.");
                }

                const payload = {
                    productos,
                    comentarios: commentsField ? commentsField.value.trim() : "",
                    usuario_id: usuarioIdField ? usuarioIdField.value.trim() : null
                };

                const response = await fetch("/api/ventas", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();

                if (!response.ok || !result.ok) {
                    throw new Error(result.mensaje || "No se pudo guardar la venta.");
                }

                buildOrderDetailFromResponse(result.lineas, result.total_pedido, result.pedido_id);
                alert(`Venta guardada correctamente. Pedido: ${result.pedido_id}`);
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