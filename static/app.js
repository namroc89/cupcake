const BASE_URL = "http://localhost:5000/api";

function generateCupcakeHTML(cupcake) {
  return `<div data-id="${cupcake.id}">
                <li>${cupcake.flavor} | ${cupcake.size} | ${cupcake.rating}</li>
                <img src="${cupcake.image}">
                </div>
                `;
}

async function showCupcakes() {
  const response = await axios.get(`${BASE_URL}/cupcakes`);

  for (let cupcakeInfo of response.data.cupcakes) {
    let newCupcake = $(generateCupcakeHTML(cupcakeInfo));
    $("#cupcakes").append(newCupcake);
  }
}

$("#new-cupcake").on("submit", async function (e) {
  e.preventDefault();

  let flavor = $("#flavor").val();
  let size = $("#size").val();
  let rating = $("#rating").val();
  let image = $("#image").val();

  const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image,
  });

  let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
  $("#cupcakes").append(newCupcake);
  $("#new-cupcake").trigger("reset");
});

showCupcakes();
