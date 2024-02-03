from flask import Flask, render_template, request, redirect, send_file
from extractors.rok import extract_rok_jobs
from extractors.wwr import extract_wwr_jobs
from file import save_to_file

app = Flask("JobScrapper")


@app.route("/")
def home():
    return render_template("home.html", name="dahl")


db = {}


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None or keyword == "":
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        rok = extract_rok_jobs(keyword)
        wwr = extract_wwr_jobs(keyword)
        jobs = rok + wwr
        db[keyword] = jobs
    count = len(jobs)
    return render_template("search.html",
                           keyword=keyword,
                           jobs=jobs,
                           count=count)


@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)


app.run("0.0.0.0")
