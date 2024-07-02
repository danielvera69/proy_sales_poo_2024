// Variable de objetos
let d = document, c = console.log
// ------------------- carga inicial de la pagina ------------------------
d.addEventListener('DOMContentLoaded', function (e) {
  // Declaracion de variables
  let $customer = d.getElementById("id_customer")
  let $detailBody = d.getElementById('detalle')
  let $product = d.getElementById('id_product')
  let $btnAdd = d.getElementById("btnAdd")
  let $btnGrabar = d.getElementById("btnGrabar")
  let $form = d.getElementById("formSale")
  let detailSale = []
  let sub=0
  // if (detail_hours.length > 0) {
  //   detailOvertime = detail_hours.map(item => {
  //     const { id: idHour, des: description, fac: factor, nh, vh: value } = item
  //     return { idHour, description, factor, nh, value }
  //   })
  //   present()
  //   totals()
  // }
  // Declaracion de metodos
  // ---------- calcula el sobretiempo y lo añade al arreglo detailOvertime[] ----------
  const calculation = (id,description, iva,price,quantify) => {
    const product = detailSale.find(prod => prod.id == id)
    if (product) {
      if (!confirm(`¿Ya existe ingresado ${product.description} =>  Desea actualizarlo?`)) return
      quantify  += product.quantify
      detailSale = detailSale.filter(prod => prod.id !== id)
    }
    sub = iva > 0 ? parseFloat((price * quantify * iva).toFixed(2)) : parseFloat((price * quantify).toFixed(2))
    detailSale.push({ id, description, price,quantify,iva, sub })
    present()
    totals()
  }
  // ------------------- actualiza el detalle del sobretiempo seleccionado -----------
  const reCalculation = (vh) => {
    detailSale = detailSale.map((item) => {
      let { id, description, iva,price,quantify } = item
      sub = iva > 0 ? parseFloat((price * quantify * iva).toFixed(2)) : parseFloat((price * quantify).toFixed(2))
      return { id, description, iva, price, quantify,sub }
    })
    present()
    totals()
  }
  // ---------------  borra el sobretiempo dado el id en el arreglo detailOvertime[] ------------
  const deleteproduct = (id) => {
    detailSale = detailSale.filter((item) => item.id !== id)
    present()
    totals()
  }
  // recorre el arreglo detailOvertime y renderiza el detalle del sobretiempo -----------
  function present() {
    c("estoy en present()")
    let detalle = d.getElementById('detalle')
    detalle.innerHTML = ""
    detailSale.forEach((product) => {
      detalle.innerHTML += `<tr>
            <td>${product.id}</td>
            <td>${product.description}</td>
            <td>${product.price}</td>
            <td>${product.quantify}</td>
            <td>💰${product.iva}</td>
            <td>💰${product.sub}</td>
            <td class="text-center ">
                <button rel="rel-delete" data-id="${product.id}" class="text-red-600 dark:text-red-500"><i class="fa-solid fa-trash"></i></button>
            </td>
          </tr>`
    });
  }
  // ----- Sumariza del arreglo detailOvertime[] y lo renderiza en la tabla de la pagina -----
  function totals() {
    const result = detailSale.reduce((acc, product) => {
      acc.iva += product.iva;
      acc.sub += product.sub;
      return acc;
    }, { iva: 0, sub: 0 });
    d.getElementById('id_subtotal').value = result.sub.toFixed(2)
    d.getElementById('id_iva').value = result.iva.toFixed(2)
    d.getElementById('id_total').value = (result.sub + result.iva).toFixed(2)
  }
  // ------------- manejo del DOM -------------
  // ---------- envia los datos del sobretiempo al backend por ajax para grabarlo ----------
  $form.addEventListener('submit', async (e) => {
    e.preventDefault()
    if (parseFloat(d.getElementById('id_total').value) > 0.00) {
      const formData = new FormData($form)
      formData.append("detail", JSON.stringify(detailSale))
      const sale = await fetchPost(location.pathname, formData)
      if (!sale.ok) return c(sale.data)
      window.location = backUrl
    } else {
      alert("!!!Ingrese horas de sobretiempo para grabar!!!")
    }
  });
  // -------- registra las horas del sobretiempo en el arreglo detailOvertime[] ---------
  $btnAdd.addEventListener('click', (e) => {
    let quantify = parseInt(d.getElementById('quantify').value)
    if (quantify > 0) {
      let idProd = parseInt($product.value)
      let price = parseFloat(d.getElementById('price').value)
      let iva = parseFloat($product.options[$product.selectedIndex].dataset.iva);
      let description = $product.options[$product.selectedIndex].text
      //factor = factor.replace(',', '.')
      calculation(typeHours, factor, hoursDescription, valueHour, numeHour)
      d.getElementById('id_nume_hours').value = ""
    } else {
      alert("Faltan datos de ingresar( horas de sobretiempo o calendario de rol")
    }
  });
  //---- por delegacion de eventos seleccionada la fila de las horas del sobretiempo ----------
  //---- y la elimina del arreglo de detailOvertime[]  ---------
  $detailBody.addEventListener('click', (e) => {
    const fil = e.target.closest('button[rel=rel-delete]')
    if (fil) deleteHours(parseInt(fil.dataset.id))
  });
});
