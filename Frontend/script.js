const suits = ['♥', '♦', '♣', '♠']; 
const values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']; 
 
let deck = []; 
let hand = []; 
 
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
 
// Function to deal 5 cards 
function dealCards() { 
    hand = []; 
    for (let i = 0; i < 2; i++) { 
        hand.push(deck.pop()); 
    } 
} 
 
// Function to display the hand 
function displayHand() { 
    const handDiv = document.getElementById('hand'); 
    handDiv.innerHTML = ''; 
    for (const card of hand) { 
        const cardDiv = document.createElement('div'); 
        cardDiv.className = 'card'; 
        cardDiv.textContent = card; 
        handDiv.appendChild(cardDiv); 
    } 
} 
 
// Event listener for the deal button 
document.getElementById('deal-button').addEventListener('click', () => { 
    createDeck(); 
    shuffleDeck(); 
    dealCards(); 
    displayHand(); 
}); 
