from flask import Flask, render_template, request
import math

app = Flask(__name__)

def calculate_poisson_probabilities(lambda_rate, max_k):
    try:
        probabilities = []
        for k in range(max_k + 1):
            prob = (math.exp(-lambda_rate) * (lambda_rate ** k)) / math.factorial(k)
            probabilities.append({
                "k": k,
                "prob": prob,
                "percentage": prob * 100
            })
        return probabilities
    except Exception as e:
        return {"error": str(e)}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            lambda_rate = float(request.form['lambda'])
            max_k = int(request.form['max_k'])

            if lambda_rate < 0 or max_k < 0:
                raise ValueError("Nilai lambda dan k harus lebih besar atau sama dengan nol.")

            probabilities = calculate_poisson_probabilities(lambda_rate, max_k)

            if isinstance(probabilities, dict) and "error" in probabilities:
                return render_template('index.html', result={"error": probabilities["error"]})

            result = {
                "lambda_rate": lambda_rate,
                "max_k": max_k,
                "probabilities": probabilities
            }
            return render_template('index.html', result=result)
        except ValueError as ve:
            return render_template('index.html', result={"error": str(ve)})
        except Exception as e:
            return render_template('index.html', result={"error": "Terjadi kesalahan: " + str(e)})
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
