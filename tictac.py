from flask import Flask, render_template_string, jsonify, request
import random

app = Flask(__name__)

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(board[i][j] != '' for i in range(3) for j in range(3))

def minimax(board, depth, is_maximizing, alpha, beta):
    """Minimax with alpha-beta pruning — always plays optimally."""
    if check_winner(board, 'O'):
        return 10 - depth
    if check_winner(board, 'X'):
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:
        best = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    best = max(best, minimax(board, depth + 1, False, alpha, beta))
                    board[i][j] = ''
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
        return best
    else:
        best = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    best = min(best, minimax(board, depth + 1, True, alpha, beta))
                    board[i][j] = ''
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
        return best

def get_best_move(board, difficulty):
    empty = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    if not empty:
        return None

    if difficulty == 'easy':
        return random.choice(empty)

    if difficulty == 'medium' and random.random() < 0.45:
        return random.choice(empty)

    # Hard: full minimax
    best_val, best_pos = float('-inf'), None
    for i, j in empty:
        board[i][j] = 'O'
        val = minimax(board, 0, False, float('-inf'), float('inf'))
        board[i][j] = ''
        if val > best_val:
            best_val, best_pos = val, (i, j)
    return best_pos

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/ai_move', methods=['POST'])
def ai_move():
    data = request.get_json(force=True)
    board = data.get('board')
    difficulty = data.get('difficulty', 'hard')

    if not board or len(board) != 3 or any(len(r) != 3 for r in board):
        return jsonify({'error': 'Invalid board'}), 400

    move = get_best_move(board, difficulty)
    if move:
        return jsonify({'row': move[0], 'col': move[1]})
    return jsonify({'row': None, 'col': None})

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Tic-Tac-Toe</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:      #0d0d1a;
  --surface: #1a1a2e;
  --surface2:#141428;
  --x:       #f06292;
  --o:       #4dd0e1;
  --text:    #e8e8f0;
  --muted:   #6b6b8a;
  --border:  #2a2a42;
  --cell:    clamp(88px, 27vw, 118px);
  --gap:     clamp(8px, 2vw, 12px);
  --r:       14px;
}

body {
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: var(--bg); color: var(--text);
  min-height: 100dvh;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: clamp(16px, 4vw, 32px) 16px;
  overflow-x: hidden;
}
body::before {
  content: ''; position: fixed; inset: 0;
  background:
    radial-gradient(ellipse 60% 40% at 25% 15%, rgba(77,208,225,.07) 0%, transparent 70%),
    radial-gradient(ellipse 60% 40% at 75% 85%, rgba(240,98,146,.07) 0%, transparent 70%);
  pointer-events: none; z-index: 0;
}

.container {
  position: relative; z-index: 1;
  width: 100%; max-width: 420px;
  display: flex; flex-direction: column;
  align-items: center; gap: clamp(14px, 3.5vw, 20px);
}

/* Header */
.title {
  font-size: clamp(1.9rem, 7vw, 2.8rem);
  font-weight: 900; letter-spacing: -.03em;
  background: linear-gradient(130deg, var(--o) 30%, var(--x));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; text-align: center;
}
.subtitle {
  font-size: .72rem; color: var(--muted);
  text-transform: uppercase; letter-spacing: .12em;
  margin-top: 3px; text-align: center;
}

/* Controls panel */
.panel {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 18px; padding: 14px 16px;
  width: 100%; display: flex; flex-direction: column; gap: 10px;
}
.ctrl-row { display: flex; align-items: center; gap: 8px; }
.ctrl-label {
  font-size: .72rem; color: var(--muted);
  text-transform: uppercase; letter-spacing: .09em; min-width: 72px;
}
.btn-group { display: flex; gap: 6px; flex: 1; }
.tog {
  flex: 1; padding: 7px 6px;
  border: 1px solid var(--border); background: transparent;
  color: var(--muted); border-radius: 9px;
  font-size: .78rem; font-weight: 600; cursor: pointer;
  transition: all .18s;
}
.tog:hover { border-color: var(--o); color: var(--text); }
.tog.on {
  background: linear-gradient(135deg, rgba(77,208,225,.18), rgba(240,98,146,.18));
  border-color: var(--o); color: var(--text);
}

/* Scoreboard */
.scoreboard {
  width: 100%; display: grid;
  grid-template-columns: 1fr 56px 1fr; gap: 8px; align-items: center;
}
.score-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 16px; padding: 13px 10px; text-align: center;
  transition: transform .25s, box-shadow .25s;
}
.score-card.xc { border-color: rgba(240,98,146,.28); }
.score-card.oc { border-color: rgba(77,208,225,.28); }
.score-card.active {
  transform: scale(1.04);
  box-shadow: 0 0 22px -4px rgba(77,208,225,.22);
}
.slabel { font-size: .65rem; color: var(--muted); text-transform: uppercase; letter-spacing: .09em; }
.ssym   { font-size: 1.35rem; font-weight: 900; margin: 3px 0 2px; line-height: 1; }
.sval   { font-size: 1.7rem;  font-weight: 800; line-height: 1; }
.xc .ssym { color: var(--x); }
.oc .ssym { color: var(--o); }
.score-mid .sval { font-size: 1.3rem; font-weight: 700; color: var(--muted); }

/* Status */
.status-row { display: flex; align-items: center; gap: 10px; min-height: 28px; }
.status { font-size: .95rem; font-weight: 600; transition: all .25s; }
.status.win  { color: var(--o); }
.status.lose { color: var(--x); }
.status.draw { color: var(--muted); }

.thinking { display: none; align-items: center; gap: 6px; font-size: .78rem; color: var(--muted); }
.thinking.on { display: flex; }
.dots { display: flex; gap: 4px; }
.dots span {
  width: 5px; height: 5px; border-radius: 50%; background: var(--o);
  animation: dp 1.2s infinite;
}
.dots span:nth-child(2) { animation-delay: .2s; }
.dots span:nth-child(3) { animation-delay: .4s; }
@keyframes dp {
  0%,80%,100% { opacity:.3; transform:scale(.75); }
  40%         { opacity: 1; transform:scale(1);   }
}

/* Board */
.board {
  display: grid;
  grid-template-columns: repeat(3, var(--cell));
  grid-template-rows:    repeat(3, var(--cell));
  gap: var(--gap);
}
.cell {
  width: var(--cell); height: var(--cell);
  background: var(--surface); border: 1.5px solid var(--border);
  border-radius: var(--r);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  font-size: calc(var(--cell) * .44); font-weight: 900; line-height: 1;
  transition: background .15s, border-color .15s, transform .15s;
  -webkit-tap-highlight-color: transparent; user-select: none;
}
.cell:hover:not(.taken) {
  background: var(--surface2); border-color: rgba(77,208,225,.45);
  transform: scale(.95);
}
.cell.taken { cursor: default; }
.cell.cx { color: var(--x); text-shadow: 0 0 18px rgba(240,98,146,.55); }
.cell.co { color: var(--o); text-shadow: 0 0 18px rgba(77,208,225,.55); }
.cell.pop { animation: pop .28s cubic-bezier(.34,1.56,.64,1); }
@keyframes pop { from { transform:scale(.4); opacity:0; } to { transform:scale(1); opacity:1; } }
.cell.win-x { background:rgba(240,98,146,.14); border-color:var(--x); animation:pulseX .55s ease forwards; }
.cell.win-o { background:rgba(77,208,225,.14);  border-color:var(--o); animation:pulseO .55s ease forwards; }
@keyframes pulseX { 50% { box-shadow:0 0 0 8px rgba(240,98,146,0); } }
@keyframes pulseO { 50% { box-shadow:0 0 0 8px rgba(77,208,225,0);  } }

/* Action buttons */
.actions { display: flex; gap: 10px; width: 100%; }
.btn {
  flex: 1; padding: 12px; border: none; border-radius: 12px;
  font-size: .88rem; font-weight: 700; cursor: pointer;
  transition: transform .15s, box-shadow .15s; letter-spacing: .02em;
}
.btn-primary {
  background: linear-gradient(135deg, #4dd0e1, #0288d1);
  color: #fff; box-shadow: 0 4px 16px rgba(77,208,225,.28);
}
.btn-primary:hover { transform:translateY(-2px); box-shadow:0 6px 22px rgba(77,208,225,.38); }
.btn-primary:active { transform:translateY(0); }
.btn-ghost { background:transparent; border:1px solid var(--border); color:var(--muted); }
.btn-ghost:hover { border-color:var(--o); color:var(--text); }

/* Confetti */
#confetti { position:fixed; inset:0; pointer-events:none; z-index:999; }
.cf { position:absolute; border-radius:2px; animation:cffall linear forwards; }
@keyframes cffall {
  from { transform:translateY(-12px) rotate(0deg);   opacity:1; }
  to   { transform:translateY(105vh) rotate(640deg); opacity:0; }
}
</style>
</head>
<body>
<div id="confetti"></div>

<div class="container">
  <div>
    <h1 class="title">Tic&#8209;Tac&#8209;Toe</h1>
    <p class="subtitle">Minimax AI &nbsp;&middot;&nbsp; Alpha&#8209;Beta Pruning</p>
  </div>

  <div class="panel">
    <div class="ctrl-row">
      <span class="ctrl-label">Mode</span>
      <div class="btn-group">
        <button class="tog on" id="m-ai"    onclick="setMode('ai')">vs AI</button>
        <button class="tog"    id="m-human" onclick="setMode('human')">vs Human</button>
      </div>
    </div>
    <div class="ctrl-row" id="diff-row">
      <span class="ctrl-label">Difficulty</span>
      <div class="btn-group">
        <button class="tog"    id="d-easy"   onclick="setDiff('easy')">Easy</button>
        <button class="tog"    id="d-medium" onclick="setDiff('medium')">Medium</button>
        <button class="tog on" id="d-hard"   onclick="setDiff('hard')">Hard</button>
      </div>
    </div>
  </div>

  <div class="scoreboard">
    <div class="score-card xc active" id="sc-x">
      <div class="slabel" id="lbl-x">You</div>
      <div class="ssym">&#10005;</div>
      <div class="sval" id="val-x">0</div>
    </div>
    <div class="score-mid">
      <span class="slabel">Draws</span>
      <div class="sval" id="val-d">0</div>
    </div>
    <div class="score-card oc" id="sc-o">
      <div class="slabel" id="lbl-o">AI</div>
      <div class="ssym">&#9675;</div>
      <div class="sval" id="val-o">0</div>
    </div>
  </div>

  <div class="status-row">
    <div class="status" id="status">Your turn</div>
    <div class="thinking" id="thinking">
      AI thinking
      <div class="dots"><span></span><span></span><span></span></div>
    </div>
  </div>

  <div class="board" id="board"></div>

  <div class="actions">
    <button class="btn btn-primary" onclick="newGame()">New Game</button>
    <button class="btn btn-ghost"   onclick="resetAll()">Reset Scores</button>
  </div>
</div>

<script>
const LINES=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
let board=[],cur='X',over=false,mode='ai',diff='hard';
let scores={X:0,O:0,d:0};

function initBoard(){
  board=Array(9).fill('');cur='X';over=false;
  const el=document.getElementById('board');el.innerHTML='';
  for(let i=0;i<9;i++){
    const c=document.createElement('div');
    c.className='cell';c.dataset.i=i;
    c.addEventListener('click',()=>onClick(i));
    el.appendChild(c);
  }
  setStatus('');updateActive();
}

function cells(){return document.querySelectorAll('.cell');}

function onClick(i){
  if(over||board[i]||(mode==='ai'&&cur==='O'))return;
  place(i,cur);
}

function place(i,p){
  board[i]=p;
  const c=cells()[i];
  c.textContent=p==='X'?'\\u2715':'\\u25cb';
  c.classList.add(p==='X'?'cx':'co','taken','pop');
  setTimeout(()=>c.classList.remove('pop'),300);
  const w=winner();
  if(w)return endGame(w);
  if(board.every(Boolean))return endGame(null);
  cur=cur==='X'?'O':'X';
  updateActive();
  setStatus(mode==='ai'?(cur==='X'?'Your turn':"AI\\'s turn"):('Player '+cur+"'s turn"));
  if(mode==='ai'&&cur==='O'&&!over)aiTurn();
}

function updateActive(){
  document.getElementById('sc-x').classList.toggle('active',cur==='X');
  document.getElementById('sc-o').classList.toggle('active',cur==='O');
}

function setStatus(txt,cls=''){
  const s=document.getElementById('status');
  s.textContent=txt;s.className='status'+(cls?' '+cls:'');
}

async function aiTurn(){
  document.getElementById('thinking').classList.add('on');
  document.getElementById('status').textContent='';
  await new Promise(r=>setTimeout(r,350));
  try{
    const mat=[[board[0]||'',board[1]||'',board[2]||''],
               [board[3]||'',board[4]||'',board[5]||''],
               [board[6]||'',board[7]||'',board[8]||'']];
    const res=await fetch('/ai_move',{method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({board:mat,difficulty:diff})});
    const d=await res.json();
    document.getElementById('thinking').classList.remove('on');
    if(d.row!==null&&!over)place(d.row*3+d.col,'O');
  }catch(e){
    document.getElementById('thinking').classList.remove('on');
    const empty=board.map((v,i)=>v?-1:i).filter(i=>i>=0);
    if(empty.length&&!over)place(empty[Math.random()*empty.length|0],'O');
  }
}

function winner(){
  for(const[a,b,c]of LINES)
    if(board[a]&&board[a]===board[b]&&board[a]===board[c])
      return{p:board[a],line:[a,b,c]};
  return null;
}

function endGame(w){
  over=true;
  document.getElementById('thinking').classList.remove('on');
  if(w){
    w.line.forEach(i=>cells()[i].classList.add('win-'+w.p.toLowerCase()));
    scores[w.p]++;updateScores();
    if(mode==='ai'){
      if(w.p==='X'){setStatus('\\uD83C\\uDF89 You win!','win');confetti();}
      else setStatus('\\uD83E\\uDD16 AI wins!','lose');
    }else{setStatus('\\uD83C\\uDF89 Player '+w.p+' wins!','win');confetti();}
  }else{
    scores.d++;updateScores();setStatus("\\uD83E\\uDD1D It\\'s a draw!",'draw');
  }
  cells().forEach(c=>c.style.cursor='default');
}

function updateScores(){
  document.getElementById('val-x').textContent=scores.X;
  document.getElementById('val-o').textContent=scores.O;
  document.getElementById('val-d').textContent=scores.d;
}

function newGame(){initBoard();}
function resetAll(){scores={X:0,O:0,d:0};updateScores();newGame();}

function setMode(m){
  mode=m;
  document.getElementById('m-ai').classList.toggle('on',m==='ai');
  document.getElementById('m-human').classList.toggle('on',m==='human');
  document.getElementById('diff-row').style.display=m==='ai'?'':'none';
  document.getElementById('lbl-x').textContent=m==='ai'?'You':'P1';
  document.getElementById('lbl-o').textContent=m==='ai'?'AI':'P2';
  newGame();
}

function setDiff(d){
  diff=d;
  ['easy','medium','hard'].forEach(x=>
    document.getElementById('d-'+x).classList.toggle('on',x===d));
  newGame();
}

function confetti(){
  const box=document.getElementById('confetti');
  const pal=['#4dd0e1','#f06292','#ffd54f','#a5d6a7','#ce93d8'];
  for(let i=0;i<70;i++){
    setTimeout(()=>{
      const p=document.createElement('div');p.className='cf';
      p.style.cssText=`left:${Math.random()*100}%;`+
        `background:${pal[Math.random()*pal.length|0]};`+
        `animation-duration:${1.4+Math.random()*.8}s;`+
        `animation-delay:${Math.random()*.4}s;`+
        `width:${6+Math.random()*6}px;height:${6+Math.random()*6}px;`+
        `border-radius:${Math.random()<.4?'50%':'2px'};`;
      box.appendChild(p);setTimeout(()=>p.remove(),2800);
    },i*18);
  }
}

initBoard();
</script>
</body>
</html>"""

if __name__ == '__main__':
    print("\\n  Open http://localhost:5000 in any browser.")
    print("  On your phone: use your PC's local IP, e.g. http://192.168.x.x:5000\\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
