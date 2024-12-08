from flask import Flask, render_template, jsonify, request
from poker_logic import PokerGame, bot_move

app = Flask(__name__)
game = PokerGame()

@app.route('/')
def index():
    return render_template('index.html',
                           player_balance=game.player_balance,  # Initial player balance
                           pot=game.pot)  # Initial pot value

@app.route('/deal', methods=['POST'])
def deal():
    player_hand = game.deal_new_hand()
    return jsonify({
        'player_hand': [card.to_dict() for card in player_hand],
        'pot': game.pot
    })

@app.route('/flop', methods=['POST'])
def flop():
    community_cards = game.deal_flop()
    if community_cards:
        return jsonify({
            'community_cards': [card.to_dict() for card in community_cards]
        })
    return jsonify({'error': 'Invalid stage'}), 400

@app.route('/turn', methods=['POST'])
def turn():
    community_cards = game.deal_turn()
    if community_cards:
        return jsonify({
            'community_cards': [card.to_dict() for card in community_cards]
        })
    return jsonify({'error': 'Invalid stage'}), 400

@app.route('/river', methods=['POST'])
def river():
    community_cards = game.deal_river()
    if community_cards:
        return jsonify({
            'community_cards': [card.to_dict() for card in community_cards]
        })
    return jsonify({'error': 'Invalid stage'}), 400

@app.route('/player_action', methods=['POST'])
def player_action():
    action = request.json.get('action')
    amount = request.json.get('amount', 0)

    if action == 'fold':
        game.bot_balance += game.pot
        game.reset_game()
        return jsonify({
            'result': 'fold',
            'player_balance': game.player_balance,
            'bot_balance': game.bot_balance
        })

    elif action == 'bet':
        amount = int(amount)
        game.player_balance -= amount
        game.pot += amount
        game.player_bet += amount

        # Get bot response
        bot_response = bot_move(game.bot_balance, game.player_bet, game.bot_bet)
        bot_action = bot_response['action']
        bot_amount = bot_response['amount']

        if bot_action == 'fold':
            game.player_balance += game.pot
            return jsonify({
                'result': 'bot_fold',
                'player_balance': game.player_balance
            })

        game.bot_balance -= bot_amount
        game.pot += bot_amount
        game.bot_bet += bot_amount

        return jsonify({
            'result': 'continue',
            'bot_action': bot_action,
            'bot_amount': bot_amount,
            'pot': game.pot,
            'player_balance': game.player_balance,
            'bot_balance': game.bot_balance
        })

    elif action == 'call':
        bet_diff = game.bot_bet - game.player_bet
        game.player_balance -= bet_diff
        game.pot += bet_diff
        game.player_bet += bet_diff

        return jsonify({
            'result': 'continue',
            'pot': game.pot,
            'player_balance': game.player_balance,
            'bot_balance': game.bot_balance
        })

    elif action == 'check':
        return jsonify({
            'result': 'continue',
            'pot': game.pot,
            'player_balance': game.player_balance,
            'bot_balance': game.bot_balance
        })

@app.route('/showdown', methods=['POST'])
def showdown():
    winner = game.determine_winner()

    if winner == 'player':
        game.player_balance += game.pot
    elif winner == 'bot':
        game.bot_balance += game.pot
    else:
        split = game.pot // 2
        game.player_balance += split
        game.bot_balance += split

    return jsonify({
        'winner': winner,
        'player_hand': [card.to_dict() for card in game.player_hand],
        'bot_hand': [card.to_dict() for card in game.bot_hand],
        'player_balance': game.player_balance,
        'bot_balance': game.bot_balance
    })

if __name__ == '__main__':
    app.run(debug=True)
