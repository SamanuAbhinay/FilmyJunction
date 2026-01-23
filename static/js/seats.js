const seatPrice = 200;
const totalAmountEl = document.getElementById("totalAmount");
const seatPriceEl = document.getElementById("seatPrice");

seatPriceEl.innerText = seatPrice;

document.querySelectorAll("input[name='seats']").forEach(seat => {
  seat.addEventListener("change", () => {
    const selected = document.querySelectorAll(
      "input[name='seats']:checked"
    ).length;

    totalAmountEl.innerText = selected * seatPrice;
  });
});
