const suits = ['♥', '♦', '♣', '♠']; 
const values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']; 
 
let deck = []; 
let hand = []; 
let communityCards = [];
 
// Function to create a deck of cards 
function createDeck() { 
    deck = []; 
    for (const suit of suits) { 
        for (const value of values) { 
            deck.push(`${value}${suit}`); 
        } 
    } 
} 
 
// Function to shuffle the deck 
function shuffleDeck() { 
    for (let i = deck.length - 1; i > 0; i--) { 
        const j = Math.floor(Math.random() * (i + 1)); 
        [deck[i], deck[j]] = [deck[j], deck[i]]; 
    } 
} 
 
// Function to deal 2 cards 
function dealCards() { 
    hand = []; 
    for (let i = 0; i < 2; i++) { 
        hand.push(deck.pop()); 
    } 
} 

// Function to deal the flop
function dealFlop() {
    communityCards = [];
    for (let i = 0; i < 3; i++) {
        communityCards.push(deck.pop());
    }
}
// Function to deal the turn
function dealTurn() {
   communityCards.push(deck.pop());
}

//Function to deal the river
function dealRiver() {
    communityCards.push(deck.pop());
}

// Function to display the hand 
function displayHand() { 
    const handDiv = document.getElementById('hand'); 
    const communityDiv = document.getElementById('community');
    handDiv.innerHTML = ''; 
    communityDiv.innerHTML = '';
    for (const card of hand) { 
        const cardDiv = document.createElement('div'); 
        cardDiv.className = 'card'; 
        cardDiv.textContent = card; 
        handDiv.appendChild(cardDiv); 
    } 

    for (const card of communityCards) { 
        const cardDiv = document.createElement('div'); 
        cardDiv.className = 'card'; 
        cardDiv.textContent = card; 
        communityDiv.appendChild(cardDiv); 
    } 
} 

 function resetBoard() {
    communityCards = [];
    const communityDiv = document.getElementById('community');
    communityDiv.innerHTML= '';
 }

 function foldGame() {
    hand = [];
    communityCards = [];
    const handDiv = document.getElementById('hand');
    const communityDiv = document.getElementById('community');
    handDiv.innerHTML = '';
    communityDiv.innerHTML= '';

    //Display fold message
    let messageDiv = document.getElementById('fold-message');
    if (!messageDiv) {
        messageDiv = document.createElement('div');
        messageDiv.id = 'fold-message';
        document.body.appendChild(messageDiv); // Appending to body or main container
    }
    messageDiv.innerHTML = 'You folded. Bot wins!';
 }

// Event listener for the deal button 
document.getElementById('deal-button').addEventListener('click', () => { 
    resetBoard();
    createDeck(); 
    shuffleDeck(); 
    dealCards(); 
    displayHand(); 

    const messageDiv = document.getElementById('fold-message');
    if (messageDiv) {
        messageDiv.remove();
    }
});

document.getElementById('flop-button').addEventListener('click', () => { 
    dealFlop();
    displayHand();
});

document.getElementById('turn-button').addEventListener('click', () => { 
    dealTurn();
    displayHand();
});

document.getElementById('river-button').addEventListener('click', () => { 
    dealRiver();
    displayHand();
});

document.getElementById('fold-button').addEventListener('click', () => { 
    foldGame();
});