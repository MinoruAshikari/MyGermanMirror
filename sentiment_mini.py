comment = input("コメントを入力してください: ")

positive_words = ["good", "great", "nice", "love", "最高", "好き", "神"]
negative_words = ["bad", "hate", "terrible", "最悪", "嫌い", "微妙"]

score = 0

for word in positive_words:
    if word in comment.lower():
        score += 1

for word in negative_words:
    if word in comment.lower():
        score -= 1

if score > 0:
    result = "ポジティブ"
elif score < 0:
    result = "ネガティブ"
else:
    result = "ニュートラル"

print("判定結果:", result)

# ===== ここが新しい部分 =====
with open("results.txt", "a", encoding="utf-8") as file:
    file.write(comment + " → " + result + "\n")

