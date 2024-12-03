let bankroll = 1000;
let pot = 0;

// Function to display cards
function displayCards(cards, containerId) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";
  cards.forEach((card) => {
    const cardDiv = document.createElement("div");
    cardDiv.className = "card";
    // Convert backend suit names to symbols
    let suit = card.suit;
    switch (card.suit) {
      case "Hearts":
        suit = "♥";
        break;
      case "Diamonds":
        suit = "♦";
        break;
      case "Clubs":
        suit = "♣";
        break;
      case "Spades":
        suit = "♠";
        break;
    }
    cardDiv.textContent = `${card.rank}${suit}`;
    container.appendChild(cardDiv);
  });
}

// Function to update game state display
function updateDisplay(data) {
  if (data.pot !== undefined) {
    pot = data.pot;
    document.getElementById("pot-amount").textContent = `Pot Amount: $${pot}`;
  }
  if (data.player_balance !== undefined) {
    bankroll = data.player_balance;
    document.getElementById("bankroll-amount").textContent =
      `Player Balance: $${bankroll}`;
  }
  updateChipDisplay();
}

// Deal new hand
async function dealNewHand() {
  try {
    const response = await fetch("/deal", { method: "POST" });
    const data = await response.json();

    displayCards(data.player_hand, "hand");
    updateDisplay(data);

    // Reset community cards
    document.getElementById("community").innerHTML = "";

    // Clear any existing messages
    const messageDiv = document.getElementById("fold-message");
    if (messageDiv) {
      messageDiv.remove();
    }
  } catch (error) {
    console.error("Error dealing new hand:", error);
  }
}

// Show flop
async function showFlop() {
  try {
    const response = await fetch("/flop", { method: "POST" });
    const data = await response.json();
    if (data.community_cards) {
      displayCards(data.community_cards, "community");
    }
  } catch (error) {
    console.error("Error showing flop:", error);
  }
}

// Show turn
async function showTurn() {
  try {
    const response = await fetch("/turn", { method: "POST" });
    const data = await response.json();
    if (data.community_cards) {
      displayCards(data.community_cards, "community");
    }
  } catch (error) {
    console.error("Error showing turn:", error);
  }
}

// Show river
async function showRiver() {
  try {
    const response = await fetch("/river", { method: "POST" });
    const data = await response.json();
    if (data.community_cards) {
      displayCards(data.community_cards, "community");
    }
  } catch (error) {
    console.error("Error showing river:", error);
  }
}

// Player fold
async function playerFold() {
  try {
    const response = await fetch("/player_action", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ action: "fold" }),
    });
    const data = await response.json();

    // Clear cards
    document.getElementById("hand").innerHTML = "";
    document.getElementById("community").innerHTML = "";

    // Display fold message
    let messageDiv = document.getElementById("fold-message");
    if (!messageDiv) {
      messageDiv = document.createElement("div");
      messageDiv.id = "fold-message";
      document.body.appendChild(messageDiv);
    }
    messageDiv.innerHTML = "You folded. Bot wins!";

    updateDisplay(data);
  } catch (error) {
    console.error("Error folding:", error);
  }
}

// Place bet
async function placeBet(amount) {
  if (amount <= bankroll) {
    try {
      const response = await fetch("/player_action", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          action: "bet",
          amount: amount,
        }),
      });
      const data = await response.json();

      updateDisplay(data);
      closeModal();

      // Handle bot response
      if (data.bot_action) {
        alert(
          `Bot ${data.bot_action}s${data.bot_amount ? " $" + data.bot_amount : ""}`,
        );
      }
    } catch (error) {
      console.error("Error placing bet:", error);
    }
  } else {
    alert("Insufficient funds!");
  }
}

// Chip display update
function updateChipDisplay() {
  const denominations = { black: 100, green: 25, blue: 10, red: 5, white: 1 };
  let remainingAmount = pot;

  if (pot === 0) {
    Object.keys(denominations).forEach((color) => {
      document.getElementById(`${color}-chip-count`).textContent = "x0";
    });
    return;
  }

  Object.entries(denominations).forEach(([color, value]) => {
    const count = Math.floor(remainingAmount / value);
    document.getElementById(`${color}-chip-count`).textContent = `x${count}`;
    remainingAmount %= value;
  });
}

// Event Listeners
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("deal-button").addEventListener("click", dealNewHand);
  document.getElementById("flop-button").addEventListener("click", showFlop);
  document.getElementById("turn-button").addEventListener("click", showTurn);
  document.getElementById("river-button").addEventListener("click", showRiver);
  document.getElementById("fold-button").addEventListener("click", playerFold);
  document.getElementById("bet-button").addEventListener("click", () => {
    document.getElementById("bet-modal").style.display = "flex";
  });

  // Bet amount buttons
  ["1", "5", "25", "50", "100"].forEach((amount) => {
    document.getElementById(`bet-${amount}`).addEventListener("click", () => {
      placeBet(parseInt(amount));
    });
  });

  document.getElementById("bet-other").addEventListener("click", () => {
    const customAmount = prompt("Enter your bet amount:");
    const amount = parseFloat(customAmount);
    if (!isNaN(amount) && amount > 0) {
      placeBet(amount);
    } else {
      alert("Please enter a valid bet amount.");
    }
  });
});

function closeModal() {
  document.getElementById("bet-modal").style.display = "none";
}

document.getElementById("check-button").addEventListener("click", async () => {
  try {
    const response = await fetch("/player_action", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ action: "check" }),
    });
    const data = await response.json();
    updateDisplay(data);
  } catch (error) {
    console.error("Error checking:", error);
  }
});

document.getElementById("call-button").addEventListener("click", async () => {
  try {
    const response = await fetch("/player_action", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ action: "call" }),
    });
    const data = await response.json();
    updateDisplay(data);
  } catch (error) {
    console.error("Error calling:", error);
  }
});

async function showdown() {
  try {
    const response = await fetch("/showdown", {
      method: "POST",
    });
    const data = await response.json();

    // Display bot's cards
    if (data.bot_hand) {
      displayBotHand(data.bot_hand);
    }

    // Show winner message
    let messageDiv = document.getElementById("fold-message");
    if (!messageDiv) {
      messageDiv = document.createElement("div");
      messageDiv.id = "fold-message";
      document.body.appendChild(messageDiv);
    }

    // Format the winner message
    let message = "";
    switch (data.winner) {
      case "player":
        message = "You win!";
        break;
      case "bot":
        message = "Bot wins!";
        break;
      case "tie":
        message = "It's a tie!";
        break;
    }
    messageDiv.innerHTML = message;

    // Update balances
    updateDisplay(data);
  } catch (error) {
    console.error("Error in showdown:", error);
  }
}

document.getElementById("showdown-button").addEventListener("click", showdown);

function displayBotHand(cards) {
  const container = document.createElement("div");
  container.id = "bot-hand";
  container.style.position = "absolute";
  container.style.top = "100px"; // Adjust position as needed
  container.style.width = "100%";
  container.style.display = "flex";
  container.style.justifyContent = "center";
  container.style.gap = "15px";
  document.querySelector(".oval").appendChild(container);
  displayCards(cards, "bot-hand");
}
