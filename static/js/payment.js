const perHead = 3000;
const cruiseName = new URLSearchParams(window.location.search).get("location") || "Selected Cruise";
document.getElementById("cruiseName").textContent = cruiseName;

const passengersInput = document.getElementById("passengers");
const amountSpan = document.getElementById("amount");

passengersInput.addEventListener("input", () => {
  const passengers = parseInt(passengersInput.value) || 0;
  amountSpan.textContent = passengers * perHead;
});

function confirmBooking() {
  const passengers = passengersInput.value;
  const total = passengers * perHead;
  const paymentMethod = document.querySelector('input[name="payment"]:checked').value;
  alert(`Booking Confirmed!\nCruise: ${cruiseName}\nPassengers: ${passengers}\nPayment: ${paymentMethod}\nTotal: ₹${total}`);
}
