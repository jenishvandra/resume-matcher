from flask import Flask, render_template, request, jsonify
from resume_matcher import calculate_match, rank_resumes

app = Flask(__name__, template_folder="templates2")

@app.route("/", methods=["GET", "POST"])
def home():
    score = None
    matched = []
    missing = []
    ranking = []

    if request.method == "POST":
        resumes = request.form.getlist("resume")
        jd = request.form["jd"]

        if len(resumes) == 1:
            score, matched, missing = calculate_match(resumes[0], jd)
        else:
            ranking = rank_resumes(resumes, jd)

    return render_template("index2.html",
                           score=score,
                           matched=matched,
                           missing=missing,
                           ranking=ranking)

@app.route("/match_score", methods=["POST"])
def match_score_api():
    data = request.get_json()
    resume = data.get("resume")
    jd = data.get("job_description")

    score, matched, missing = calculate_match(resume, jd)

    return jsonify({
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing
    })

@app.route("/rank_resumes", methods=["POST"])
def rank_api():
    data = request.get_json()
    resumes = data.get("resumes")
    jd = data.get("job_description")

    results = rank_resumes(resumes, jd)

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)