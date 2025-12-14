from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    table = None
    analysis = []

    if request.method == "POST":
        file = request.files["file"]
        if file:
            path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(path)

            df = pd.read_csv(path)

            # Table (same as Treeview)
            table = df.to_html(index=False, classes="table table-bordered")

            # Analysis (same logic you already use)
            for sub in df.columns[1:]:
                analysis.append({
                    "subject": sub,
                    "average": round(df[sub].mean(), 2),
                    "highest": df[sub].max(),
                    "lowest": df[sub].min(),
                    "topper": df.loc[df[sub].idxmax(), "Name"]
                })

    return render_template("index.html", table=table, analysis=analysis)

if __name__ == "__main__":
    app.run(debug=True)
