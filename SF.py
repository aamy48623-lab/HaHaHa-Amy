<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>猜數字進階版</title>

<style>
  body {
    font-family: Arial;
    background: linear-gradient(to right, #74ebd5, #ACB6E5);
    text-align: center;
    padding: 50px;
  }

  .game-box {
    background: white;
    padding: 30px;
    border-radius: 20px;
    display: inline-block;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  }

  h1 {
    margin-bottom: 10px;
  }

  select, input, button {
    margin: 10px;
    padding: 10px;
    font-size: 16px;
  }

  button {
    background-color: orange;
    border: none;
    cursor: pointer;
    border-radius: 10px;
  }

  #result {
    font-size: 20px;
    margin-top: 15px;
  }

  #lives {
    color: red;
    font-weight: bold;
  }
</style>
</head>

<body>

<div class="game-box">
  <h1>🎮 猜數字升級版</h1>

  <label>選擇難度：</label>
  <select id="level">
    <option value="50">簡單 (1~50)</option>
    <option value="100" selected>普通 (1~100)</option>
    <option value="500">困難 (1~500)</option>
  </select>

  <br>

  <input type="number" id="guess" placeholder="輸入數字">
  <br>

  <button onclick="checkGuess()">猜！</button>
  <button onclick="restartGame()">重新開始</button>

  <p id="result"></p>
  <p>剩餘次數：<span id="lives">5</span></p>
</div>

<script>
  let answer;
  let lives;

  function startGame() {
    let max = document.getElementById("level").value;
    answer = Math.floor(Math.random() * max) + 1;
    lives = 5;
    document.getElementById("lives").innerHTML = lives;
    document.getElementById("result").innerHTML = "";
  }

  function checkGuess() {
    let guess = document.getElementById("guess").value;
    let result = document.getElementById("result");

    if (lives <= 0) return;

    lives--;
    document.getElementById("lives").innerHTML = lives;

    if (guess == answer) {
      result.innerHTML = "🎉 猜對了！";
    } else if (lives == 0) {
      result.innerHTML = "💀 遊戲結束！答案是 " + answer;
    } else if (guess > answer) {
      result.innerHTML = "📉 太大了！";
    } else {
      result.innerHTML = "📈 太小了！";
    }
  }

  function restartGame() {
    startGame();
  }

  startGame();
</script>

</body>
</html>
